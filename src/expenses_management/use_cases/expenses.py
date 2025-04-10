from datetime import datetime
from typing import Any

from exceptions import DoesNotExistError
from expenses_management.services.currency import CurrencyService
from repositories.sqlalchemy.container import SQLAlchemyUnitOfWork


class BaseExpenseUseCase:
    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self.uow = uow


class RetrieveExpensesUseCase(BaseExpenseUseCase):
    async def __call__(self, start_date: str = None, end_date: str = None) -> list[dict]:
        filters = {}

        if start_date and end_date:
            filters["start_date"] = datetime.strptime(start_date, "%d.%m.%Y")
            filters["end_date"] = datetime.strptime(end_date, "%d.%m.%Y")
            
        expenses = await self.uow.expenses.list(**filters)
        expenses_list = [
            {
                "id": exp.id,
                "title": exp.title,
                "amount_uah": exp.amount_uah,
                "amount_usd": exp.amount_usd,
                "date": exp.date.strftime("%d.%m.%Y"),
            }
            for exp in expenses
        ]
        return expenses_list


class CreateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, title: str, amount_uah: float, date: str) -> dict:
        usd_rate = CurrencyService.get_usd_rate()
        amount_usd = amount_uah / usd_rate
        date_obj = datetime.strptime(date, "%d.%m.%Y")
        expense = {"title": title, "amount_uah": amount_uah, "amount_usd": amount_usd, "date": date_obj}
        new_expense = await self.uow.expenses.create(expense)
        return {"message": "Expense added", "id": new_expense.id}


class DeleteExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int) -> dict[str, Any]:
        expense = await self.uow.expenses.retrieve(expense_id)

        if expense is None:
            raise DoesNotExistError()

        await self.uow.expenses.delete(expense_id)
        return {"message": f"Expense {expense_id} deleted"}


class UpdateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int, title: str, amount_uah: float) -> dict:
        expense = await self.uow.expenses.retrieve(expense_id)

        if not expense:
            raise DoesNotExistError()

        usd_rate = CurrencyService.get_usd_rate()
        amount_usd = amount_uah / usd_rate
        updated_data = {"title": title, "amount_uah": amount_uah, "amount_usd": amount_usd}
        await self.uow.expenses.update(expense_id, updated_data)
        return {"message": f"Expense {expense_id} updated"}
