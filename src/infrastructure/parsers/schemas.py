from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, ConfigDict, Field, field_validator


MONEY = Decimal("0.01")

_MONEY_FIELDS = [
    "usag_intl_actv_amt", "usag_national_actv_amt", "usag_air_actv_amt",
    "usag_sms_actv_amt", "usag_gprs_actv_amt",
    "irom_local_actv_amt", "irom_sms_actv_amt", "irom_gprs_actv_amt",
    "irom_server_actv_amt",
    "nrom_local_actv_amt", "nrom_sms_actv_amt", "nrom_gprs_actv_amt",
    "nrom_server_actv_amt",
    "rc_pp_actv_amt", "rc_soc_actv_amt", "disc_actv_amt",
    "oc_ot_price", "latepym",
    "subtotal_amount", "trs_lo_rc_uc_amt", "trs_lo_oc_amt",
    "vat", "total_amount",
]


class ChargeEntrySchema(BaseModel):
    """Детальная строка или итог — общая схема для всех форматов."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    ctn: str | None = Field(default=None, description="Номер телефона")
    ban: str | None = Field(default=None, description="Договор")
    ben: str | None = Field(default=None, description="Группа счетов")

    period_start_date: date
    period_end_date: date

    offer_description: str | None = None

    usag_intl_actv_amt: Decimal = Decimal("0")
    usag_national_actv_amt: Decimal = Decimal("0")
    usag_air_actv_amt: Decimal = Decimal("0")
    usag_sms_actv_amt: Decimal = Decimal("0")
    usag_gprs_actv_amt: Decimal = Decimal("0")

    irom_local_actv_amt: Decimal = Decimal("0")
    irom_sms_actv_amt: Decimal = Decimal("0")
    irom_gprs_actv_amt: Decimal = Decimal("0")
    irom_server_actv_amt: Decimal = Decimal("0")

    nrom_local_actv_amt: Decimal = Decimal("0")
    nrom_sms_actv_amt: Decimal = Decimal("0")
    nrom_gprs_actv_amt: Decimal = Decimal("0")
    nrom_server_actv_amt: Decimal = Decimal("0")

    rc_pp_actv_amt: Decimal = Decimal("0")
    rc_soc_actv_amt: Decimal = Decimal("0")
    disc_actv_amt: Decimal = Decimal("0")
    oc_ot_price: Decimal = Decimal("0")
    latepym: Decimal = Decimal("0")

    subtotal_amount: Decimal = Decimal("0")
    trs_lo_rc_uc_amt: Decimal = Decimal("0")
    trs_lo_oc_amt: Decimal = Decimal("0")
    vat: Decimal = Decimal("0")
    total_amount: Decimal = Decimal("0")

    @field_validator("period_start_date", "period_end_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        """Поддержка DD.MM.YYYY, YYYY-MM-DD и date."""
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            v = v.strip()
            if "." in v:
                d, m, y = v.split(".")
                return date(int(y), int(m), int(d))
            return date.fromisoformat(v)
        return v

    @field_validator(*_MONEY_FIELDS, mode="before")
    @classmethod
    def empty_to_zero(cls, v):
        if v is None or v == "":
            return Decimal("0")
        return v

    @field_validator(*_MONEY_FIELDS, mode="after")
    @classmethod
    def round_money(cls, v: Decimal) -> Decimal:
        return v.quantize(MONEY, rounding=ROUND_HALF_UP)


class ChargesFile(BaseModel):
    """Результат парсинга любого источника."""

    model_config = ConfigDict(populate_by_name=True)

    source_type: str
    entries: list[ChargeEntrySchema] = Field(default_factory=list)
    summary: ChargeEntrySchema | None = None


class CallRecordSchema(BaseModel):
    """Один звонок из детализации (XLSX)."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    started_at: datetime = Field(alias="Начало вызова")
    dialed_number: str = Field(alias="Набранный №")
    caller_number: str = Field(alias="№ звонящего")   # наш номер
    city: str | None = Field(default=None, alias="Город")
    duration_sec: int = Field(default=0, alias="Длит-ть розн.")
    rate: Decimal = Field(default=Decimal("0"), alias="Тариф розн.")
    amount: Decimal = Field(default=Decimal("0"), alias="Сумма розн.")
    currency: str = Field(default="рубль", alias="Валюта розн.")

    @field_validator("started_at", mode="before")
    @classmethod
    def parse_dt(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            return datetime.fromisoformat(v.strip())
        return v

    @field_validator("dialed_number", "caller_number", mode="before")
    @classmethod
    def to_str(cls, v):
        # Excel может отдать число — приводим к строке без .0
        if isinstance(v, float) and v.is_integer():
            return str(int(v))
        return str(v).strip()

    @field_validator("duration_sec", mode="before")
    @classmethod
    def to_int(cls, v):
        if v in (None, ""):
            return 0
        return int(float(v))