from typing import Any, Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from repositories.sqlalchemy.container import SQLAlchemyUnitOfWork

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_unit_of_work() -> Generator[SQLAlchemyUnitOfWork, Any, None]:
    async with Session() as session:
        yield SQLAlchemyUnitOfWork(session)
