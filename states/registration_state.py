from aiogram.filters.state import State, StatesGroup


class FSMRegistration(StatesGroup):
    name = State()
    phone = State()
    date_of_birth = State()
