import asyncio
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from bot.handlers.expenses.add import (
    process_expense_amount,
    process_expense_date,
    process_expense_title,
    start_adding_expense,
)
from bot.handlers.expenses.delete import process_delete_expense_id, start_delete_expense
from bot.handlers.expenses.edit import (
    process_edit_expense_amount,
    process_edit_expense_id,
    process_edit_expense_title,
    start_edit_expense,
)
from bot.handlers.expenses.report import (
    process_expense_report_end_date,
    process_expense_report_start_date,
    start_generating_expense_report,
)
from bot.handlers.menu import start_command
from bot.services import http_client
from bot.states.expense import ExpenseStates
from config import settings


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)

    dispatcher.message.register(start_command, Command("start"))
    dispatcher.message.register(start_adding_expense, F.text == "Додати статтю витрат")
    dispatcher.message.register(start_generating_expense_report, F.text == "Отримати звіт витрат")
    dispatcher.message.register(start_delete_expense, F.text == "Видалити статтю")
    dispatcher.message.register(start_edit_expense, F.text == "Відредагувати статтю")

    dispatcher.message.register(process_expense_title, ExpenseStates.title)
    dispatcher.message.register(process_expense_date, ExpenseStates.date)
    dispatcher.message.register(process_expense_amount, ExpenseStates.amount_uah)

    dispatcher.message.register(process_expense_report_start_date, ExpenseStates.report_start)
    dispatcher.message.register(process_expense_report_end_date, ExpenseStates.report_end)

    dispatcher.message.register(process_delete_expense_id, ExpenseStates.delete_id)

    dispatcher.message.register(process_edit_expense_id, ExpenseStates.edit_id)
    dispatcher.message.register(process_edit_expense_title, ExpenseStates.edit_title)
    dispatcher.message.register(process_edit_expense_amount, ExpenseStates.edit_amount)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await dispatcher.storage.close()
        await bot.session.close()


async def shutdown():
    """ " Shut down http client (use 1 session for all requests in order to reduce time of requests)"""
    await http_client.close()


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(shutdown())
