from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date, DateTime, ForeignKey, Integer, Numeric, String,
    UniqueConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FieldDictionary(Base):
    """Справочник: машинное имя поля → его title из формы/XML."""

    __tablename__ = "field_dictionary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity: Mapped[str] = mapped_column(
        String(32), nullable=False, index=True,
        comment="Сущность: charge_entry, charges_summary, charges_report",
    )
    field_name: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True,
        comment="Машинное имя колонки",
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Человекочитаемое описание из формы",
    )

    __table_args__ = (
        UniqueConstraint("entity", "field_name", name="uq_field_dictionary"),
    )


class ChargesAmountsMixin:
    """Общие колонки начислений. В comment — title из XML."""

    usag_intl_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="Международные звонки",
    )
    usag_national_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="Междугородние звонки",
    )
    usag_air_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="Местные звонки",
    )
    usag_sms_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="SMS/MMS",
    )
    usag_gprs_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="GPRS",
    )

    irom_local_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Международный роуминг Эфирное время (начисления партнера)",
    )
    irom_sms_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Международный роуминг SMS (начисления партнера)",
    )
    irom_gprs_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Международный роуминг GPRS (начисления партнера)",
    )
    irom_server_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Начисления за международный роуминг",
    )

    nrom_local_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="В поездках по России Эфирное время",
    )
    nrom_sms_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="В поездках по России SMS",
    )
    nrom_gprs_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="В поездках по России Мобильный интернет",
    )
    nrom_server_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Начисления за трафик в поездках по России",
    )

    rc_pp_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Абонентская плата по тарифному плану",
    )
    rc_soc_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Абонентская плата за доп. услуги",
    )
    disc_actv_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="Скидки",
    )
    oc_ot_price: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Разовые начисления (Операции)",
    )
    latepym: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="Пени",
    )

    subtotal_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="Итого по строке",
    )
    trs_lo_rc_uc_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Перенесенные начисления по абон. плате и звонкам",
    )
    trs_lo_oc_amt: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0,
        comment="Перенесенные значения за операции",
    )
    vat: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="НДС",
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=0, comment="Всего по строке",
    )


class ChargeEntry(ChargesAmountsMixin, Base):
    """Детальная строка: один номер в одном отчёте."""

    __tablename__ = "charge_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("charges_reports.id", ondelete="CASCADE"), index=True
    )
    ctn: Mapped[str] = mapped_column(
        String(32), nullable=False, index=True, comment="Номер телефона",
    )
    ban: Mapped[str | None] = mapped_column(
        String(32), index=True, comment="Договор",
    )
    ben: Mapped[str | None] = mapped_column(
        String(16), comment="Группа счетов",
    )
    offer_description: Mapped[str | None] = mapped_column(
        String(255), comment="Тарифный план",
    )

    report: Mapped["ChargesReport"] = relationship(back_populates="entries")


class ChargesSummary(ChargesAmountsMixin, Base):
    """Итоговая строка по счёту (без ctn)."""

    __tablename__ = "charge_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("charges_reports.id", ondelete="CASCADE"),
        unique=True, index=True,
    )
    ben: Mapped[str | None] = mapped_column(
        String(16), comment="Группа счетов",
    )

    report: Mapped["ChargesReport"] = relationship(back_populates="summary")


class ChargesReport(Base):
    """Шапка: одна загрузка (период + источник)."""

    __tablename__ = "charges_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ban: Mapped[str | None] = mapped_column(
        String(32), index=True, comment="Договор",
    )
    period_start: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="Дата начала периода",
    )
    period_end: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="Дата окончания периода",
    )
    source_type: Mapped[str] = mapped_column(
        String(32), nullable=False, index=True,
        comment="Тип источника (формат файла)",
    )
    source_file: Mapped[str | None] = mapped_column(
        String(255), comment="Имя загруженного файла",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
        comment="Дата создания записи",
    )

    entries: Mapped[list[ChargeEntry]] = relationship(
        back_populates="report", cascade="all, delete-orphan", lazy="selectin",
    )
    summary: Mapped[ChargesSummary | None] = relationship(
        back_populates="report", cascade="all, delete-orphan",
        uselist=False, lazy="selectin",
    )