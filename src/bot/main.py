import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram import F

import sys, os

print(sys.path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.services import http_client

from config import settings

from bot.handlers.expense import add_expense_start, process_title, process_date, process_amount, report_start, process_report_start, process_report_end, start_delete_expense, process_delete_expense_id, start_edit_expense, process_edit_expense_id, process_edit_expense_title, process_edit_expense_amount
from bot.handlers.menu import start_command
from bot.states.expense import ExpenseStates


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    storage = MemoryStorage()
    dispatcher = Dispatcher( storage=storage)

    dispatcher.message.register(start_command, Command("start"))
    dispatcher.message.register(add_expense_start, F.text == "Додати статтю витрат")
    dispatcher.message.register(process_title, ExpenseStates.title)
    dispatcher.message.register(process_date, ExpenseStates.date)
    dispatcher.message.register(process_amount, ExpenseStates.amount)
    dispatcher.message.register(report_start, F.text == "Отримати звіт витрат")
    dispatcher.message.register(process_report_start, ExpenseStates.report_start)
    dispatcher.message.register(process_report_end, ExpenseStates.report_end)
    dispatcher.message.register(start_delete_expense, F.text == "Видалити статтю")
    dispatcher.message.register(process_delete_expense_id, ExpenseStates.delete_id)
    dispatcher.message.register(start_edit_expense, F.text == "Відредагувати статтю")
    dispatcher.message.register(process_edit_expense_id, ExpenseStates.edit_id)
    dispatcher.message.register(process_edit_expense_title, ExpenseStates.edit_title)
    dispatcher.message.register(process_edit_expense_amount, ExpenseStates.edit_amount)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await dispatcher.storage.close()
        await bot.session.close()


async def shutdown():
    await http_client.close()

    
if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(shutdown())