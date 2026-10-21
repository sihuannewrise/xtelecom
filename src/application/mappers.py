from __future__ import annotations

from datetime import date

from src.infrastructure.db.models import (
    ChargeEntry as ChargeEntryORM,
    ChargesReport as ChargesReportORM,
    ChargesSummary as ChargesSummaryORM,
)
from src.infrastructure.parsers.schemas import ChargeEntrySchema, ChargesFile


_NON_ORM_ENTRY_FIELDS = {"period_start_date", "period_end_date"}
_NON_ORM_SUMMARY_FIELDS = {"ctn", "ban", "period_start_date", "period_end_date"}


def entry_to_orm(e: ChargeEntrySchema, report_id: int) -> ChargeEntryORM:
    data = e.model_dump(exclude=_NON_ORM_ENTRY_FIELDS)
    return ChargeEntryORM(report_id=report_id, **data)


def summary_to_orm(s: ChargeEntrySchema, report_id: int) -> ChargesSummaryORM:
    data = s.model_dump(exclude=_NON_ORM_SUMMARY_FIELDS, exclude_none=True)
    return ChargesSummaryORM(report_id=report_id, **data)


def report_to_orm(payload: ChargesFile, source_file: str | None) -> ChargesReportORM:
    first = payload.entries[0]
    return ChargesReportORM(
        ban=first.ban,
        period_start=first.period_start_date,
        period_end=first.period_end_date,
        source_type=payload.source_type,
        source_file=source_file,
    )


def totals_rows(
    raw: list[tuple],
    period_start: date,
    period_end: date,
) -> list[dict]:
    return [
        {
            "ctn": ctn,
            "ban": ban,
            "period_start": period_start,
            "period_end": period_end,
            "total_amount": total,
            "vat": vat,
            "sources_count": sources,
        }
        for ctn, ban, total, vat, sources in raw
    ]
