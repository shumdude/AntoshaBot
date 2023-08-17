from aiogram import Router, Bot
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, URLInputFile
from aiogram.exceptions import TelegramNetworkError, TelegramBadRequest
from fluentogram import TranslatorRunner
from bot.settings import NO_PHOTO
from bot.settings import get_product_caption
from bot.keyboards import catalog_kb
from bot.database import Product
from bot.database.db_requests import *

catalog_router: Router = Router()  # Инициализируем роутер уровня модуля


# Выгрузить из БД каталог товаров
@catalog_router.message(Command(commands='get'))
async def process_get_command(message: Message, i18n: TranslatorRunner):
    catalog_list = await get_catalog()
    for product in catalog_list:
        text = f"{product.name}, {product.price}, {product.url}, {product.photo}"
        await message.answer(text=text)


# В будущем реализовать хранение всех фотографий каталога в формате telegram_photo_id, т.к. URL - затратно по времени
async def catalog_process(callback: CallbackQuery, product: Product):
    product_caption = get_product_caption(product)
    try:
        photo = URLInputFile(product.url)
        media = InputMediaPhoto(media=photo, caption=product_caption)
        await callback.message.edit_media(media=media, reply_markup=catalog_kb)
    except TelegramNetworkError:
        photo = URLInputFile(NO_PHOTO)
        media = InputMediaPhoto(media=photo, caption=product_caption)
        await callback.message.edit_media(media=media, reply_markup=catalog_kb)
    except TelegramBadRequest:
        await callback.message.edit_caption(caption=product_caption, reply_markup=catalog_kb)


@catalog_router.message(Command(commands='catalog'))
async def process_catalog_command(message: Message, bot: Bot):
    await update_page(page=1, user_id=message.from_user.id)
    product: Product = await get_product(0)
    product_caption = get_product_caption(product)
    try:
        photo = URLInputFile(product.url)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=product_caption, reply_markup=catalog_kb)
    except TelegramNetworkError:
        photo = URLInputFile(NO_PHOTO)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=product_caption, reply_markup=catalog_kb)


@catalog_router.callback_query(Text(text=['back']))
async def back_button_press(callback: CallbackQuery, ):
    await update_page(page=1, user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.answer()


@catalog_router.callback_query(Text(startswith=['right']))
async def right_button_press(callback: CallbackQuery):
    page = await get_page(callback.from_user.id)
    catalog_length = await get_catalog_length()
    if page < catalog_length:
        product = await get_product(page)
        await update_page(page=page + 1, user_id=callback.from_user.id)
        await catalog_process(callback, product)
    await callback.answer()


@catalog_router.callback_query(Text(text=['left']))
async def left_button_press(callback: CallbackQuery):
    page = await get_page(callback.from_user.id)
    if page > 1:
        product = await get_product(page - 2)
        await update_page(page=page - 1, user_id=callback.from_user.id)
        await catalog_process(callback, product)
    await callback.answer()

# @router.message(Command(commands='load'))
# async def process_load_command(message: Message):
#     data = services.get_data_from_json()
#     database.load_data_in_db(data)
#     await message.answer(text=LEXICON['/load'], reply_markup=None)
