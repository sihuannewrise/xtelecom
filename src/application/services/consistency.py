from __future__ import annotations

from datetime import date
from decimal import Decimal

from src.application.ports import (
    EntryRepositoryProtocol,
    TotalRepositoryProtocol,
)


class ConsistencyService:
    """Проверка: агрегат по номеру = сумма детальных строк по всем источникам."""

    def __init__(
        self,
        entries: EntryRepositoryProtocol,
        totals: TotalRepositoryProtocol,
    ):
        self.entries = entries
        self.totals = totals

    async def check(
        self, period_start: date, period_end: date
    ) -> list[dict]:
        aggregates = await self.totals.list_by_period(period_start, period_end)
        by_ctn = {a.ctn: a for a in aggregates}

        issues: list[dict] = []
        for ctn, agg in by_ctn.items():
            raw = await self.entries.sum_by_ctn_and_period(
                [ctn], period_start, period_end
            )
            fact = sum((r[2] or Decimal("0")) for r in raw)
            agg_total = agg.total_amount or Decimal("0")
            if fact != agg_total:
                issues.append(
                    {
                        "ctn": ctn,
                        "fact_total": fact,
                        "aggregate_total": agg_total,
                        "diff": fact - agg_total,
                    }
                )
        return issues
