from aiogram.filters.state import State, StatesGroup


class FSMRemind(StatesGroup):
    telegram_id = State()
    test = State()
    date = State()
    time = State()
    answer_time = State()
