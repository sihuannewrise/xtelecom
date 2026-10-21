from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Period:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"Начало периода {self.start} позже окончания {self.end}")


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str = "RUB"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
