from sqlalchemy import select, insert, delete

from app.database import session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with session_maker() as session:
            print(filter_by)
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with session_maker() as session:
            stmt = insert(cls.model).values(**values)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(cls, id: int):
        async with session_maker() as session:
            stmt = delete(cls.model).filter_by(id=id)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_elements(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            results = await session.execute(query)
            results = results.scalars()
            return results

