from __future__ import annotations

from datetime import date
from decimal import Decimal

from src.application.ports import TotalRepositoryProtocol


class AnalyticsService:
    def __init__(self, totals: TotalRepositoryProtocol):
        self.totals = totals

    async def top_numbers(
        self, period_start: date, period_end: date, limit: int = 10
    ) -> list[dict]:
        rows = await self.totals.list_by_period(period_start, period_end)
        rows.sort(key=lambda r: r.total_amount or Decimal("0"), reverse=True)
        return [
            {
                "ctn": r.ctn,
                "ban": r.ban,
                "total_amount": r.total_amount,
                "vat": r.vat,
                "sources_count": r.sources_count,
            }
            for r in rows[:limit]
        ]
