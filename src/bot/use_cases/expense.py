from bot.services.api import APIService
from bot.services.file import FileService


class BaseExpenseUseCase:
    def __init__(self, api_service: APIService, file_service: FileService):
        self.api_service = api_service
        self.file_service = file_service


class CreateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_data: dict) -> str:
        result = await self.api_service.create_expense(expense_data)
        return result["message"]


class RetrieveReportUseCase(BaseExpenseUseCase):
    async def __call__(self, start_date: str, end_date: str) -> tuple[str, str]:
        expenses = await self.api_service.get_expenses(start_date, end_date)
        report_filename = self.file_service.generate_excel_file(expenses)
        total_amount = self.file_service.get_total_amount(expenses)
        return report_filename, f"Загальна сума: {total_amount} UAH"


class DeleteExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int) -> tuple[str, str]:
        result = await self.api_service.delete_expense(expense_id)
        return result["message"]


class UpdateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int, expense_data: dict) -> str:
        result = await self.api_service.update_expense(expense_id, expense_data)
        return result["message"]


class GenerateExpensesReportUseCase(BaseExpenseUseCase):
    async def __call__(self) -> str:
        expenses = await self.api_service.get_expenses()
        filename = self.file_service.generate_excel_file(expenses)
        return filename
