from typing import List, Dict, Any
from datetime import datetime
from bot.services.api import APIService
from bot.services.file import FileService

class BaseExpenseUseCase:
    def __init__(self, api_service: APIService, file_service: FileService):
        self.api_service = api_service
        self.file_service = file_service

class CreateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, title: str, amount_uah: float, date: str) -> str:
        # try:
        datetime.strptime(date, "%d.%m.%Y")  # Валідація дати
        result = await self.api_service.create_expense(title, amount_uah, date)
        print("rrrrrr", result)
        return result["message"]
        # except ValueError:
        #     raise ValueError("Невірний формат дати. Використовуйте dd.mm.YYYY")
        # except Exception as e:
        #     raise RuntimeError(f"Помилка при створенні витрати: {str(e)}")

class GetReportUseCase(BaseExpenseUseCase): #?
    async def __call__(self, start_date: str, end_date: str) -> tuple[str, str]:
        try:
            datetime.strptime(start_date, "%d.%m.%Y")
            datetime.strptime(end_date, "%d.%m.%Y")
            expenses = await self.api_service.get_expenses(start_date, end_date)
            filename = self.file_service.generate_excel_file(expenses)
            total_amount = self.file_service.get_total_amount(expenses)
            return filename, f"Загальна сума: {total_amount} UAH"
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте dd.mm.YYYY")
        except Exception as e:
            raise RuntimeError(f"Помилка при отриманні звіту: {str(e)}")

class DeleteExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int) -> tuple[str, str]:
        # try:
            # expenses = self.api_service.get_expenses()
            # filename = self.file_service.generate_excel_file(expenses)
        result = await self.api_service.delete_expense(expense_id)
        return result["message"]
        # except Exception as e:
        #     raise RuntimeError(f"Помилка при видаленні витрати: {str(e)}")

class UpdateExpenseUseCase(BaseExpenseUseCase):
    async def __call__(self, expense_id: int, title: str, amount_uah: float) -> tuple[str, str]:
        try:
            # expenses = self.api_service.get_expenses()
            # filename = self.file_service.generate_excel_file(expenses)
            result = await self.api_service.update_expense(expense_id, title, amount_uah)
            return result["message"]
        except Exception as e:
            raise RuntimeError(f"Помилка при редагуванні витрати: {str(e)}")
        

class GenerateExpensesReportUseCase(BaseExpenseUseCase):
    async def __call__(self) -> str:
        """Генерує Excel-файл із витратами."""
        try:
            expenses = await self.api_service.get_expenses()
            filename = self.file_service.generate_excel_file(expenses)
            return filename
        except Exception as e: #?
            raise RuntimeError(f"Помилка при генерації звіту: {str(e)}")