from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message, WebAppData
from bot.keyboards import web_kb, remove_kb


web_app_router: Router = Router()  # Инициализируем роутер уровня модуля


@web_app_router.message(Command(commands='web'))
async def web_app_data_receive(message: Message):
    await message.answer('На', reply_markup=web_kb)


@web_app_router.message(Command(commands='web_cancel'))
async def web_app_data_receive(message: Message):
    await message.answer('Пока', reply_markup=remove_kb)


@web_app_router.message(F.content_type.in_(ContentType.WEB_APP_DATA))
async def web_app_data_receive(message: Message):
    await message.answer(message.web_app_data.data)
