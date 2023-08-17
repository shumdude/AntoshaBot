import datetime
from aiogram.filters import Command, StateFilter
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from fluentogram import TranslatorRunner
from bot.database import User
from bot.database.db_requests import registration, get_user
from bot.filters import ContactFilter, DateFilter
from bot.keyboards import contact_kb, remove_kb
from bot.states import FSMRegistration

registration_router: Router = Router()  # Инициализируем роутер уровня модуля


@registration_router.message(Command(commands='profile'))
async def process_cancel_command_state(message: Message, i18n: TranslatorRunner):
    user: User = await get_user(message.from_user.id)
    await message.answer(i18n.profile(username=user.name, phone=user.phone, date_of_birth=user.date_of_birth))


# Отмена
@registration_router.message(Command(commands='cancel_registration'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await message.answer(i18n.registration.cancel())
    await state.clear()


# Точка входа - registration
@registration_router.message(Command(commands='registration'), StateFilter(default_state))
async def process_fsm_command(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await message.answer(i18n.registration.start())
    await state.set_state(FSMRegistration.name)


# Имя
@registration_router.message(StateFilter(FSMRegistration.name))
async def process_name(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await state.update_data(name=message.text)
    await message.answer(text=i18n.registration.phone(), reply_markup=contact_kb)
    await state.set_state(FSMRegistration.phone)


# Номер телефона
@registration_router.message(StateFilter(FSMRegistration.phone), ContactFilter())
async def process_phone(message: Message, state: FSMContext, i18n: TranslatorRunner):
    # Логика номера телефона
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(text=i18n.registration.date_of_birth(), reply_markup=remove_kb)
    await state.set_state(FSMRegistration.date_of_birth)


# Точка выхода - Дата рождения
@registration_router.message(StateFilter(FSMRegistration.date_of_birth), DateFilter())
async def process_date_of_birth(message: Message, state: FSMContext, i18n: TranslatorRunner, date: datetime.date):
    await state.update_data(date_of_birth=date)
    data = await state.get_data()
    await registration(user_id=message.from_user.id,
                       date_of_birth=data["date_of_birth"],
                       name=data["name"],
                       phone=data["phone"])
    await state.clear()
    await message.answer(i18n.registration.ok())
