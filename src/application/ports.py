from __future__ import annotations

from datetime import date
from typing import Protocol

from src.infrastructure.db.models import (
    ChargeEntry,
    ChargesReport,
    ChargesSummary,
    ChargeTotalByCtn,
)


class ReportRepositoryProtocol(Protocol):
    async def get(
        self,
        ban: str | None,
        period_start: date,
        period_end: date,
        source_type: str,
    ) -> ChargesReport | None: ...

    async def add(self, report: ChargesReport) -> ChargesReport: ...

    async def delete(self, report: ChargesReport) -> None: ...


class EntryRepositoryProtocol(Protocol):
    async def bulk_add(self, entries: list[ChargeEntry]) -> None: ...

    async def list_by_report(self, report_id: int) -> list[ChargeEntry]: ...

    async def sum_by_ctn_and_period(
        self,
        ctn_list: list[str],
        period_start: date,
        period_end: date,
    ) -> list[tuple[str, str | None, object, object, int]]:
        """Возвращает (ctn, ban, total_amount, vat, sources_count)."""
        ...


class SummaryRepositoryProtocol(Protocol):
    async def add(self, summary: ChargesSummary) -> None: ...


class TotalRepositoryProtocol(Protocol):
    async def upsert_many(self, rows: list[dict]) -> None: ...

    async def delete_all(self) -> None: ...

    async def list_by_period(
        self, period_start: date, period_end: date
    ) -> list[ChargeTotalByCtn]: ...


class UnitOfWorkProtocol(Protocol):
    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class ParserProtocol(Protocol):
    def parse(self, content: bytes) -> "ChargesFileProtocol": ...


class ChargesFileProtocol(Protocol):
    """Минимальный контракт результата парсинга — чтобы ports не зависел от Pydantic."""

    source_type: str
    entries: list
    summary: object | None
