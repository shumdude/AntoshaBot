import datetime
from aiogram.filters import Command, StateFilter
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from bot.database import User
from bot.database.db_requests import registration, get_user
from bot.filters import ContactFilter, DateFilter
from bot.keyboards import contact_kb, remove_kb
from bot.settings import LEXICON
from bot.states import FSMRegistration

registration_router: Router = Router()  # Инициализируем роутер уровня модуля


@registration_router.message(Command(commands='info'))
async def process_cancel_command_state(message: Message):
    user: User = await get_user(message.from_user.id)
    text: str = f"Имя: {user.name}\n\nНомер: {user.phone}\n\nДата рождения: {user.date_of_birth}"
    await message.answer(text=text)


# Отмена
@registration_router.message(Command(commands='cancel_registration'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Ок. Не регистрируем.')
    await state.clear()


# Точка входа - registration
@registration_router.message(Command(commands='registration'), StateFilter(default_state))
async def process_fsm_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["/registration"])
    await state.set_state(FSMRegistration.name)


# Имя
@registration_router.message(StateFilter(FSMRegistration.name))
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Отлично. Поделитесь номером телефона с помощью кнопки ниже:', reply_markup=contact_kb)
    await state.set_state(FSMRegistration.phone)


# Номер телефона
@registration_router.message(StateFilter(FSMRegistration.phone), ContactFilter())
async def process_phone(message: Message, state: FSMContext):
    # Логика номера телефона
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(text='Супер! Последний шаг. Введите дату рождения в формате дд.мм.гггг. Например, 10.06.2001',
                         reply_markup=remove_kb)
    await state.set_state(FSMRegistration.date_of_birth)


# Точка выхода - Дата рождения
@registration_router.message(StateFilter(FSMRegistration.date_of_birth), DateFilter())
async def process_date_of_birth(message: Message, state: FSMContext, date: datetime.date):
    await state.update_data(date_of_birth=date)
    data = await state.get_data()
    await registration(user_id=message.from_user.id,
                               date_of_birth=data["date_of_birth"],
                               name=data["name"],
                               phone=data["phone"])
    await state.clear()
    await message.answer(text="Вы зарегистрированы! Ура!\n\nДля просмотра вашего аккаунта используйте /info")
