import re
from datetime import datetime
from functools import wraps
from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message


class ExpenseValidator:
    @staticmethod
    def validate_title(value: str) -> tuple[bool, str | None]:
        if not value.strip():
            return False, "Назва не може бути порожньою!"
        if len(value) > 100:
            return False, "Назва занадто довга (макс. 100 символів)!"
        if not re.match(r"^[a-zA-Zа-яА-Я0-9\s]+$", value):
            return False, "Назва може містити лише букви, цифри та пробіли!"
        return True, None

    @staticmethod
    def validate_amount(value: str) -> tuple[bool, str | None]:
        try:
            amount = float(value)
            if amount <= 0:
                return False, "Сума має бути більше 0!"
            if amount > 1_000_000_000:
                return False, "Сума занадто велика (макс. 1,000,000,000 UAH)!"
            return True, None
        except ValueError:
            return False, "Введіть коректну суму (наприклад, 150.50)!"

    @staticmethod
    def validate_date(value: str) -> tuple[bool, str | None]:
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
            return False, "Формат дати: dd.mm.YYYY (наприклад, 19.03.2025)!"  # ?
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True, None
        except ValueError:
            return False, "Неправильна дата!"

    @staticmethod
    def validate_id(value: str) -> tuple[bool, str | None]:
        try:
            expense_id = int(value)
            if expense_id <= 0:
                return False, "ID має бути більше 0!"
            return True, None
        except ValueError:
            return False, "Введіть коректний ID (ціле число)!"


def validate_input(validator: Callable[[str], tuple[bool, str | None]]):
    def decorator(handler: Callable):
        @wraps(handler)
        async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
            value = message.text
            is_valid, error = validator(value)
            if not is_valid:
                await message.answer(f"{error}\nПовторіть введення:")
                return
            return await handler(message, state, *args, **kwargs)

        return wrapper

    return decorator
