from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types.message import Message

from bot.handlers.menu import show_main_menu
from bot.services.api import APIService
from bot.services.file import FileService
from bot.services.http_client import http_client
from bot.services.validator import ExpenseValidator, validate_input
from bot.states.expense import ExpenseStates
from bot.use_cases.expense import (
    CreateExpenseUseCase,
    DeleteExpenseUseCase,
    GenerateExpensesReportUseCase,
    GetReportUseCase,
    UpdateExpenseUseCase,
)

api_service = APIService(http_client)
file_service = FileService()


# Додавання витрат
async def start_adding_expense(message: Message, state: FSMContext):
    await message.answer("Введіть назву статті витрат:\n\nНаприклад: 'Щомісячна сплата за інтернет'")
    await state.set_state(ExpenseStates.title)


@validate_input(ExpenseValidator.validate_title)
async def process_expense_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(ExpenseStates.date)
    await message.answer(
        f"Введіть дату (dd.mm.YYYY):\n\nНаприклад: '{datetime.now().strftime('%d.%m.%Y')}'"
    )  # ? make var?


@validate_input(ExpenseValidator.validate_date)
async def process_expense_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(ExpenseStates.amount)
    await message.answer("Введіть суму (UAH):")


@validate_input(ExpenseValidator.validate_amount)
async def process_expense_amount(message: Message, state: FSMContext, bot: Bot):
    # try:
    amount = float(message.text)
    data = await state.get_data()
    use_case = CreateExpenseUseCase(api_service, file_service)
    result = await use_case(data["title"], amount, data["date"])
    await message.answer(result)
    await state.clear()
    await show_main_menu(bot, message.chat.id)
    # except ValueError as e:#?
    #     await message.answer(str(e) if "формат" in str(e) else "Введіть коректну суму!")
    # except Exception as e:
    #     await message.answer(str(e))


# Звіт
async def start_generating_expense_report(message: Message, state: FSMContext):
    await state.set_state(ExpenseStates.report_start)
    await message.answer("Введіть дату початку (dd.mm.YYYY):")


@validate_input(ExpenseValidator.validate_date)
async def process_expense_report_start_date(message: Message, state: FSMContext):
    await state.update_data(start=message.text)
    await state.set_state(ExpenseStates.report_end)
    await message.answer("Введіть дату кінця (dd.mm.YYYY):")


@validate_input(ExpenseValidator.validate_date)
async def process_expense_report_end_date(message: Message, state: FSMContext, bot: Bot):
    # try:
    data = await state.get_data()
    use_case = GetReportUseCase(api_service, file_service)
    filename, caption = await use_case(data["start"], message.text)

    document = FSInputFile(filename, filename=filename)
    await message.answer_document(document, caption=caption)

    file_service.cleanup_file(filename)
    await state.clear()
    await show_main_menu(bot, message.chat.id)
    # except ValueError as e:
    #     await message.answer(str(e))
    # except Exception as e:
    #     await message.answer(str(e))


async def start_delete_expense(message: Message, state: FSMContext):
    use_case = GenerateExpensesReportUseCase(api_service, file_service)
    try:
        filename = await use_case()
        document = FSInputFile(filename, filename=filename)
        await message.answer_document(document, caption="Виберіть ID витрати для видалення:")
        file_service.cleanup_file(filename)
        await state.set_state(ExpenseStates.delete_id)
    except RuntimeError as e:
        await message.answer(str(e))
        await state.clear()


@validate_input(ExpenseValidator.validate_id)
async def process_delete_expense_id(message: Message, state: FSMContext, bot: Bot):
    try:
        expense_id = int(message.text)
        use_case = DeleteExpenseUseCase(api_service, file_service)
        result = await use_case(expense_id)
        await message.answer(result)
        await state.clear()
        await show_main_menu(bot, message.chat.id)
    except ValueError:
        await message.answer("Введіть коректний ID!")
    except RuntimeError as e:
        await message.answer(f"Помилка: {str(e)}")
        await state.clear()


async def start_edit_expense(message: Message, state: FSMContext):
    """Запускає процес редагування витрати, надсилаючи звіт із витратами."""
    use_case = GenerateExpensesReportUseCase(api_service, file_service)
    # try:
    filename = await use_case()
    document = FSInputFile(filename, filename=filename)
    await message.answer_document(document, caption="Виберіть ID витрати для редагування:")
    file_service.cleanup_file(filename)
    await state.set_state(ExpenseStates.edit_id)
    # except RuntimeError as e:
    #     await message.answer(str(e))
    #     await state.clear()


@validate_input(ExpenseValidator.validate_id)
async def process_edit_expense_id(message: Message, state: FSMContext):
    """Обробляє введений ID і показує поточні дані витрати."""
    # try:
    expense_id = int(message.text)
    await state.update_data(edit_id=expense_id)
    expenses = await api_service.get_expenses()
    expense = next((e for e in expenses if e["id"] == expense_id), None)
    if expense:
        await message.answer(f"Поточні дані: {expense['title']} - {expense['amount_uah']} UAH")
        await state.set_state(ExpenseStates.edit_title)
        await message.answer("Введіть нову назву:")
    else:
        await message.answer("Витрата не знайдена!")
        await state.clear()
    # except ValueError:
    #     await message.answer("Введіть коректний ID!")


@validate_input(ExpenseValidator.validate_title)
async def process_edit_expense_title(message: Message, state: FSMContext):
    """Зберігає нову назву витрати і запитує суму."""
    await state.update_data(title=message.text)
    await state.set_state(ExpenseStates.edit_amount)
    await message.answer("Введіть нову суму (UAH):")


@validate_input(ExpenseValidator.validate_amount)
async def process_edit_expense_amount(
    message: Message,
    state: FSMContext,
    bot: Bot,
):
    """Виконує оновлення витрати з новими даними."""
    # try:
    amount_uah = float(message.text)
    data = await state.get_data()
    use_case = UpdateExpenseUseCase(api_service, file_service)
    result = await use_case(data["edit_id"], data["title"], amount_uah)
    await message.answer(result)
    await state.clear()
    await show_main_menu(bot, message.chat.id)
    # except ValueError:
    #     await message.answer("Введіть коректну суму!")
    # except RuntimeError as e:
    #     await message.answer(f"Помилка: {str(e)}")
    #     await state.clear()
