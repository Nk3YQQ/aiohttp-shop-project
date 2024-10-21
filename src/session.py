from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def create(async_session: async_sessionmaker[AsyncSession], obj) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add(obj)
