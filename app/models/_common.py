from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class BaseWithPK(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class SupplementaryBase(BaseWithPK):
    __abstract__ = True
    name: Mapped[str] = mapped_column(String(50), unique=True)

    def __repr__(self) -> str:
        if self.description:
            return (
                f'<{self.__class__.__name__} ({self.name}-{self.description})>'
            )
        else:
            return f'<{self.__class__.__name__} ({self.name})>'


# class EntityBase(Base):
#     __abstract__ = True

#     address: Mapped[Optional[str]] = mapped_column(String(200))
#     status: Mapped[Optional[EntityStatus]] = mapped_column(String(20))

#     actuality_date: Mapped[Optional[datetime]]
#     registration_date: Mapped[Optional[datetime]]
#     liquidation_date: Mapped[Optional[datetime]]

#     is_archived: Mapped[Optional[bool]] = mapped_column(
#         server_default=text('FALSE'))

#     def __repr__(self) -> str:
#         return f'<{self.__class__.__name__} ({self.name})>'
