from sqlalchemy import and_, delete, select, update
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
        await self.session.refresh(instance)
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
        query = select(self.model_class)
        conditions = []
        for key, value in filters.items():
            if "__gte" in key:
                field = getattr(self.model_class, key.split("__gte")[0])
                conditions.append(field >= value)
            elif "__lte" in key:
                field = getattr(self.model_class, key.split("__lte")[0])
                conditions.append(field <= value)
            else:
                query = query.filter_by(**{key: value})
        if conditions:
            query = query.where(and_(*conditions))
        result = await self.session.execute(query)
        return result.scalars().all()
