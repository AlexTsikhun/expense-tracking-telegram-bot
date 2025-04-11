from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types.message import Message

from bot.handlers.menu import show_main_menu
from bot.services import api_service, file_service
from bot.services.validator import ExpenseValidator, validate_input
from bot.states.expense import ExpenseStates
from bot.use_cases.expense import DeleteExpenseUseCase, GenerateExpensesReportUseCase


async def start_delete_expense(message: Message, state: FSMContext):
    await state.clear()

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
