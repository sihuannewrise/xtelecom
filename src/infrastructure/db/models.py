from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ChargesReport(Base):
    """Шапка отчёта: одна загрузка файла (период + источник)."""

    __tablename__ = "charges_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ban: Mapped[str | None] = mapped_column(String(32), index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    period_end: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    source_file: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    entries: Mapped[list[ChargeEntry]] = relationship(
        back_populates="report",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    summary: Mapped[ChargesSummary | None] = relationship(
        back_populates="report",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "ban", "period_start", "period_end", "source_type",
            name="uq_report_period_source",
        ),
    )


class _MoneyColumns:
    """Только колонки начислений — без методов."""

    usag_intl_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    usag_national_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    usag_air_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    usag_sms_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    usag_gprs_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)

    irom_local_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    irom_sms_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    irom_gprs_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    irom_server_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)

    nrom_local_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    nrom_sms_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    nrom_gprs_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    nrom_server_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)

    rc_pp_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    rc_soc_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    disc_actv_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    oc_ot_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    latepym: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)

    subtotal_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    trs_lo_rc_uc_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    trs_lo_oc_amt: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    vat: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)


class ChargeEntry(_MoneyColumns, Base):
    """Детальная строка: один номер в одном отчёте."""

    __tablename__ = "charge_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("charges_reports.id", ondelete="CASCADE"), index=True
    )
    ctn: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    ban: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    ben: Mapped[str | None] = mapped_column(String(16))
    offer_description: Mapped[str | None] = mapped_column(String(255))

    report: Mapped[ChargesReport] = relationship(back_populates="entries")

    __table_args__ = (
        UniqueConstraint("report_id", "ctn", name="uq_entry_report_ctn"),
    )


class ChargesSummary(_MoneyColumns, Base):
    """Итоговая строка по счёту (без ctn)."""

    __tablename__ = "charge_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("charges_reports.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    ben: Mapped[str | None] = mapped_column(String(16))

    report: Mapped[ChargesReport] = relationship(back_populates="summary")


class ChargeTotalByCtn(Base):
    """Агрегат по номеру за период: сумма по всем источникам."""

    __tablename__ = "charge_totals_by_ctn"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ctn: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    ban: Mapped[str | None] = mapped_column(String(32), index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    period_end: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    vat: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    sources_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "ctn", "period_start", "period_end",
            name="uq_total_ctn_period",
        ),
    )
