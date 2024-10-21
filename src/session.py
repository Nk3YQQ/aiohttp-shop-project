from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def create(async_session: async_sessionmaker[AsyncSession], obj) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add(obj)


async def read_all(async_session: async_sessionmaker[AsyncSession], model, skip: int = 0, limit: int = 10):
    async with async_session() as session:
        stmt = select(model).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()


async def read_one(async_session: async_sessionmaker[AsyncSession], model, instance_id: int):
    async with async_session() as session:
        stmt = select(model).where(model.id == instance_id)
        result = await session.execute(stmt)
        return result.scalars().first()


async def update_obj(async_session: async_sessionmaker[AsyncSession], model, instance_id: int, data: dict):
    async with async_session() as session:
        stmt = update(model).where(model.id == instance_id).values(**data)
        await session.execute(stmt)
        await session.commit()


async def delete_obj(async_session: async_sessionmaker[AsyncSession], model, instance_id: int):
    async with async_session() as session:
        stmt = delete(model).where(model.id == instance_id)
        await session.execute(stmt)
        await session.commit()
