from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from bot.handlers.menu import show_main_menu
from bot.services import api_service, file_service
from bot.services.validator import ExpenseValidator, validate_input
from bot.states.expense import ExpenseStates
from bot.use_cases.expense import CreateExpenseUseCase


# Додавання витрат
async def start_adding_expense(message: Message, state: FSMContext):
    await state.clear()

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
