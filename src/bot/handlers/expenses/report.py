from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types.message import Message

from bot.handlers.menu import show_main_menu
from bot.services import api_service, file_service
from bot.services.validator import ExpenseValidator, validate_input
from bot.states.expense import ExpenseStates
from bot.use_cases.expense import RetrieveReportUseCase


async def start_generating_expense_report(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Введіть дату початку (dd.mm.YYYY):")
    await state.set_state(ExpenseStates.report_start)


@validate_input(ExpenseValidator.validate_date)
async def process_expense_report_start_date(message: Message, state: FSMContext):
    await state.update_data(start=message.text)
    await state.set_state(ExpenseStates.report_end)
    await message.answer("Введіть дату кінця (dd.mm.YYYY):")


@validate_input(ExpenseValidator.validate_date)
async def process_expense_report_end_date(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    use_case = RetrieveReportUseCase(api_service, file_service)
    filename, caption = await use_case(data["start"], message.text)

    document = FSInputFile(filename, filename=filename)
    await message.answer_document(document, caption=caption)

    file_service.cleanup_file(filename)
    await state.clear()
    await show_main_menu(bot, message.chat.id)
