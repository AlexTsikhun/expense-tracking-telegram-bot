from exceptions import DoesNotExistError
from expenses_management.services.currency import CurrencyService
from expenses_management.utils import format_date
from repositories.sqlalchemy.container import SQLAlchemyUnitOfWork


class BaseExpenseUseCase:
    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self.uow = uow


class RetrieveExpensesUseCase(BaseExpenseUseCase):
    async def __call__(self, filters: dict) -> list[dict]:
        query_filters = {}
        if filters["start_date"]:
            query_filters["date__gte"] = filters["start_date"]
        if filters["end_date"]:
            query_filters["date__lte"] = filters["end_date"]

        async with self.uow:
            expenses = await self.uow.expenses.list(**query_filters)

        expenses_list = [
            {
                "id": expense.id,
                "title": expense.title,
                "amount_uah": expense.amount_uah,
                "amount_usd": expense.amount_usd,
                "date": format_date(expense.date),
            }
            for expense in expenses
        ]
        return expenses_list


class CreateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_date: dict) -> dict:
        usd_rate = CurrencyService.get_usd_rate()
        amount_uah = expense_date["amount_uah"]
        amount_usd = amount_uah / usd_rate

        expense = {
            "title": expense_date["title"],
            "amount_uah": amount_uah,
            "amount_usd": amount_usd,
        }

        async with self.uow:
            new_expense = await self.uow.expenses.create(expense)

        return {
            "id": new_expense.id,
            "title": new_expense.title,
            "amount_uah": new_expense.amount_uah,
            "amount_usd": new_expense.amount_usd,
            "date": format_date(new_expense.date),
            "message": "Витрату успішно створено",
        }


class UpdateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int, expense_data: dict) -> dict:
        async with self.uow:
            expense = await self.uow.expenses.retrieve(expense_id)

            if not expense:
                raise DoesNotExistError()

            amount_uah = expense_data["amount_uah"]

            usd_rate = CurrencyService.get_usd_rate()
            amount_usd = amount_uah / usd_rate
            updated_data = {"title": expense_data["title"], "amount_uah": amount_uah, "amount_usd": amount_usd}
            await self.uow.expenses.update(expense_id, updated_data)
            return expense_data | {"message": "Витрату успішно оновлено"}


class DeleteExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int) -> dict:
        async with self.uow:
            expense = await self.uow.expenses.retrieve(expense_id)

            if expense is None:
                raise DoesNotExistError()

            await self.uow.expenses.delete(expense_id)

            return {"message": "Витрату успішно видалено"}
