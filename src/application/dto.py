from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ReportCreatedResponse(BaseModel):
    report_id: int
    source_type: str


class TopNumberItem(BaseModel):
    ctn: str
    ban: str | None
    total_amount: Decimal
    vat: Decimal
    sources_count: int


class TopNumbersResponse(BaseModel):
    period_start: date
    period_end: date
    items: list[TopNumberItem]


class ConsistencyIssue(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ctn: str
    fact_total: Decimal = Field(description="Сумма по строкам")
    aggregate_total: Decimal = Field(description="Значение из charge_totals_by_ctn")
    diff: Decimal = Field(description="fact_total - aggregate_total")


class ConsistencyResponse(BaseModel):
    period_start: date
    period_end: date
    issues: list[ConsistencyIssue]
    consistent: bool
