from datetime import datetime


def format_date(date: datetime.date) -> str:
    return date.strftime("%d.%m.%Y")


def get_current_date() -> str:
    return datetime.now().strftime("%d.%m.%Y")
