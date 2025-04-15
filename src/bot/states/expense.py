from aiogram.fsm.state import State, StatesGroup


class ExpenseStates(StatesGroup):
    title = State()
    date = State()
    amount_uah = State()
    report_start = State()
    report_end = State()
    delete_id = State()
    edit_id = State()
    edit_title = State()
    edit_amount = State()
