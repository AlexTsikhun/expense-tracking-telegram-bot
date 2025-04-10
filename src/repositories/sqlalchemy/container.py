from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy.expenses import ExpensesRepository


class SQLAlchemyUnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.expenses = ExpensesRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()
