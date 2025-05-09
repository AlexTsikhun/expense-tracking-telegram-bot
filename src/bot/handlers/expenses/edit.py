from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types.message import Message

from bot.handlers.menu import show_main_menu
from bot.services import api_service, file_service
from bot.services.validator import ExpenseValidator, validate_input
from bot.states.expense import ExpenseStates
from bot.use_cases.expense import GenerateExpensesReportUseCase, UpdateExpenseUseCase


async def start_edit_expense(message: Message, state: FSMContext):
    await state.clear()

    use_case = GenerateExpensesReportUseCase(api_service, file_service)
    filename = await use_case()

    document = FSInputFile(filename, filename=filename)
    await message.answer_document(document, caption="Виберіть ID витрати для редагування:")
    file_service.cleanup_file(filename)
    await state.set_state(ExpenseStates.edit_id)


@validate_input(ExpenseValidator.validate_id)
async def process_edit_expense_id(message: Message, state: FSMContext):
    expense_id = int(message.text)
    await state.update_data(edit_id=expense_id)
    expenses = await api_service.get_expenses()
    expense = next((expense for expense in expenses if expense["id"] == expense_id), None)

    if expense:
        await message.answer(f"Поточні дані: {expense['title']} - {expense['amount_uah']} UAH")
        await state.set_state(ExpenseStates.edit_title)
        await message.answer("Введіть нову назву:")
    else:
        await message.answer("Витрата не знайдена!")
        await state.clear()


@validate_input(ExpenseValidator.validate_title)
async def process_edit_expense_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(ExpenseStates.edit_amount)
    await message.answer("Введіть нову суму (UAH):")


@validate_input(ExpenseValidator.validate_amount)
async def process_edit_expense_amount(
    message: Message,
    state: FSMContext,
    bot: Bot,
):
    amount_uah = float(message.text)
    data = await state.get_data()
    expense_data = data | {"amount_uah": amount_uah}
    expense_id = expense_data.pop("edit_id")

    use_case = UpdateExpenseUseCase(api_service, file_service)
    result = await use_case(expense_id, expense_data)

    await message.answer(result)
    await state.clear()
    await show_main_menu(bot, message.chat.id)
