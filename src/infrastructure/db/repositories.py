from datetime import date

from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    ChargeEntry,
    ChargesReport,
    ChargesSummary,
    ChargeTotalByCtn,
)


class ChargesReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
        self,
        ban: str | None,
        period_start: date,
        period_end: date,
        source_type: str,
    ) -> ChargesReport | None:
        return await self.session.scalar(
            select(ChargesReport).where(
                ChargesReport.ban == ban,
                ChargesReport.period_start == period_start,
                ChargesReport.period_end == period_end,
                ChargesReport.source_type == source_type,
            )
        )

    async def add(self, report: ChargesReport) -> ChargesReport:
        self.session.add(report)
        await self.session.flush()
        return report

    async def delete(self, report: ChargesReport) -> None:
        await self.session.delete(report)
        await self.session.flush()


class ChargeEntryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_add(self, entries: list[ChargeEntry]) -> None:
        self.session.add_all(entries)
        await self.session.flush()

    async def list_by_report(self, report_id: int) -> list[ChargeEntry]:
        result = await self.session.scalars(
            select(ChargeEntry).where(ChargeEntry.report_id == report_id)
        )
        return list(result)

    async def sum_by_ctn_and_period(
        self,
        ctn_list: list[str],
        period_start: date,
        period_end: date,
    ) -> list[tuple]:
        if not ctn_list:
            return []
        stmt = (
            select(
                ChargeEntry.ctn,
                ChargeEntry.ban,
                func.coalesce(func.sum(ChargeEntry.total_amount), 0),
                func.coalesce(func.sum(ChargeEntry.vat), 0),
                func.count(func.distinct(ChargesReport.source_type)),
            )
            .join(ChargesReport, ChargesReport.id == ChargeEntry.report_id)
            .where(
                ChargeEntry.ctn.in_(ctn_list),
                ChargesReport.period_start == period_start,
                ChargesReport.period_end == period_end,
            )
            .group_by(ChargeEntry.ctn, ChargeEntry.ban)
        )
        return list((await self.session.execute(stmt)).all())


class ChargesSummaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, summary: ChargesSummary) -> None:
        self.session.add(summary)
        await self.session.flush()


class ChargeTotalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_many(self, rows: list[dict]) -> None:
        if not rows:
            return
        stmt = pg_insert(ChargeTotalByCtn).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_total_ctn_period",
            set_={
                "total_amount": stmt.excluded.total_amount,
                "vat": stmt.excluded.vat,
                "sources_count": stmt.excluded.sources_count,
                "ban": stmt.excluded.ban,
                "updated_at": func.now(),
            },
        )
        await self.session.execute(stmt)

    async def delete_all(self) -> None:
        await self.session.execute(delete(ChargeTotalByCtn))

    async def list_by_period(
        self, period_start: date, period_end: date
    ) -> list[ChargeTotalByCtn]:
        result = await self.session.scalars(
            select(ChargeTotalByCtn).where(
                ChargeTotalByCtn.period_start == period_start,
                ChargeTotalByCtn.period_end == period_end,
            )
        )
        return list(result)
