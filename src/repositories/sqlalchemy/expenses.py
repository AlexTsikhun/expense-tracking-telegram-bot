from expenses_management.models import Expense
from repositories.sqlalchemy.repository import SQLAlchemyRepository


class ExpensesRepository(SQLAlchemyRepository):
    model_class = Expense
