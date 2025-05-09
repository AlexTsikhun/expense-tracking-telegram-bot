from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types.message import Message
from httpx import HTTPStatusError

from bot.handlers.menu import show_main_menu
from bot.services import api_service, file_service
from bot.services.validator import ExpenseValidator, validate_input
from bot.states.expense import ExpenseStates
from bot.use_cases.expense import DeleteExpenseUseCase, GenerateExpensesReportUseCase


async def start_delete_expense(message: Message, state: FSMContext):
    await state.clear()

    use_case = GenerateExpensesReportUseCase(api_service, file_service)
    filename = await use_case()
    document = FSInputFile(filename, filename=filename)
    await message.answer_document(document, caption="Виберіть ID витрати для видалення:")
    file_service.cleanup_file(filename)
    await state.set_state(ExpenseStates.delete_id)


@validate_input(ExpenseValidator.validate_id)
async def process_delete_expense_id(message: Message, state: FSMContext, bot: Bot):
    expense_id = int(message.text)

    use_case = DeleteExpenseUseCase(api_service, file_service)
    try:
        result = await use_case(expense_id)
    except HTTPStatusError:
        result = "Виникла помилка при видаленні витрати. Можливо такої витрати не існує."

    await message.answer(result)
    await state.clear()
    await show_main_menu(bot, message.chat.id)
