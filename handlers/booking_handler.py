from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from settings import LEXICON
from database import Request

from keyboards.booking_keyboard import GoodsCallbackFactory

booking_router: Router = Router()  # Инициализируем роутер уровня модуля


@booking_router.message(Command(commands='booking'))
async def booking_start_process(message: Message, bot: Bot):
    await message.answer(LEXICON['/booking'])


@booking_router.callback_query(GoodsCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory):
    await callback.message.answer(
        text=f'Категория товаров: {callback_data.category_id}\n' \
             f'Подкатегория товаров: {callback_data.subcategory_id}\n' \
             f'Товар: {callback_data.item_id}')
    await callback.answer()
