from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from .counteragent import CounterAgent


class Company(Base):
    """
    Расширение контрагента: помечает его как наше общество,
    от имени которого мы работаем. Доп. атрибуты нашего юрлица.
    """
    __tablename__ = 'company'

    id: Mapped[int] = mapped_column(
        ForeignKey('counteragent.id', ondelete='CASCADE'),
        primary_key=True,
    )

    full_name: Mapped[Optional[str]] = mapped_column(String(300))
    head_company_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('company.id')
    )

    counteragent: Mapped[CounterAgent] = relationship(
        back_populates='company'
    )

    def __repr__(self) -> str:
        return f'<Company ({self.counteragent.name})>'
