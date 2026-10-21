import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config import get_engine
from src.infrastructure.db.seed import seed_field_dictionary


async def _seed() -> None:
    engine = get_engine()
    async with AsyncSession(engine) as session:
        count = await seed_field_dictionary(session)
        print(f"field_dictionary: обновлено {count} строк")
    await engine.dispose()


def seed_dictionary() -> None:
    asyncio.run(_seed())
