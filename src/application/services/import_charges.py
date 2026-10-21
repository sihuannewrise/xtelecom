from __future__ import annotations

from src.application import mappers
from src.application.ports import (
    EntryRepositoryProtocol,
    ReportRepositoryProtocol,
    SummaryRepositoryProtocol,
    TotalRepositoryProtocol,
    UnitOfWorkProtocol,
)
from src.infrastructure.parsers.schemas import ChargesFile


class ImportChargesService:
    """
    Оркестрация импорта: проверить дубль, сохранить отчёт + строки + итог,
    пересчитать агрегат по затронутым номерам. Зависит только от протоколов.
    """

    def __init__(
        self,
        reports: ReportRepositoryProtocol,
        entries: EntryRepositoryProtocol,
        summaries: SummaryRepositoryProtocol,
        totals: TotalRepositoryProtocol,
        uow: UnitOfWorkProtocol,
    ):
        self.reports = reports
        self.entries = entries
        self.summaries = summaries
        self.totals = totals
        self.uow = uow

    async def import_file(
        self,
        payload: ChargesFile,
        source_file: str | None = None,
        *,
        replace_existing: bool = False,
    ) -> int:
        if not payload.entries:
            raise ValueError("Файл не содержит детальных строк")

        first = payload.entries[0]
        period_start = first.period_start_date
        period_end = first.period_end_date

        existing = await self.reports.get(
            first.ban, period_start, period_end, payload.source_type
        )
        if existing is not None:
            if not replace_existing:
                raise ValueError(
                    f"Отчёт {first.ban} за {period_start}–{period_end} "
                    f"({payload.source_type}) уже существует"
                )
            await self.reports.delete(existing)

        report = await self.reports.add(mappers.report_to_orm(payload, source_file))

        await self.entries.bulk_add(
            [mappers.entry_to_orm(e, report.id) for e in payload.entries]
        )

        if payload.summary is not None:
            await self.summaries.add(
                mappers.summary_to_orm(payload.summary, report.id)
            )

        await self._recalc_totals(
            ctn_list=[e.ctn for e in payload.entries],
            period_start=period_start,
            period_end=period_end,
        )

        await self.uow.commit()
        return report.id

    async def _recalc_totals(self, ctn_list, period_start, period_end) -> None:
        raw = await self.entries.sum_by_ctn_and_period(
            ctn_list, period_start, period_end
        )
        await self.totals.upsert_many(
            mappers.totals_rows(raw, period_start, period_end)
        )
