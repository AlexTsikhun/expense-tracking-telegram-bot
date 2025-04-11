from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram import Bot

async def show_main_menu(bot: Bot, chat_id: int):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Додати статтю витрат"),
                KeyboardButton(text="Отримати звіт витрат")
            ],
            [
                KeyboardButton(text="Видалити статтю"),
                KeyboardButton(text="Відредагувати статтю")
            ]
        ],
        resize_keyboard=True
    )
    await bot.send_message(chat_id, "Виберіть опцію:", reply_markup=keyboard)

async def start_command(message: Message, bot: Bot):
    await show_main_menu(bot, message.chat.id)
    