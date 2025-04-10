from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model_class = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict):
        instance = self.model_class(**data)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def retrieve(self, reference):
        query = select(self.model_class).where(self.model_class.id == reference)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, reference, data: dict):
        query = (
            update(self.model_class)
            .where(self.model_class.id == reference)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(query)
        return result.rowcount

    async def delete(self, reference):
        query = (
            delete(self.model_class)
            .where(self.model_class.id == reference)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(query)
        return result.rowcount

    async def list(self, **filters):
        query = select(self.model_class).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalars().all()
