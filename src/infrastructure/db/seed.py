from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from .field_titles import TITLE_DICTIONARY
from .models import FieldDictionary


async def seed_field_dictionary(session: AsyncSession) -> int:
    """Вставляет/обновляет title'ы в field_dictionary. Возвращает число строк."""
    rows = [
        {"entity": entity, "field_name": field, "title": title}
        for entity, fields in TITLE_DICTIONARY.items()
        for field, title in fields.items()
    ]
    if not rows:
        return 0

    stmt = pg_insert(FieldDictionary).values(rows)
    stmt = stmt.on_conflict_do_update(
        constraint="uq_field_dictionary",
        set_={"title": stmt.excluded.title},
    )
    await session.execute(stmt)
    await session.commit()
    return len(rows)
