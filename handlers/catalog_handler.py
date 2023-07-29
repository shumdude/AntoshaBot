from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, URLInputFile, InputMedia
from aiogram.exceptions import TelegramNetworkError, TelegramBadRequest
from settings import NO_PHOTO
from settings import LEXICON, get_product_caption
from keyboards import catalog_kb
from database import Request

catalog_router: Router = Router()  # Инициализируем роутер уровня модуля


# Выгрузить из БД каталог товаров
@catalog_router.message(Command(commands='get'))
async def process_get_command(message: Message, request: Request):
    await message.answer(text=LEXICON['/get'])
    catalog_list = await request.get_catalog()
    for el in catalog_list:
        text = ', '.join([str(x) for x in el])
        await message.answer(text=text)


# В будущем реализовать хранение всех фотографий каталога в формате telegram_photo_id, т.к. URL - затратно по времени
async def catalog_process(callback: CallbackQuery, product):
    photo_url = product[3]
    product_caption = get_product_caption(product)
    try:
        photo = URLInputFile(photo_url)
        media = InputMediaPhoto(media=photo, caption=product_caption)
        await callback.message.edit_media(media=media, reply_markup=catalog_kb)
    except TelegramNetworkError:
        photo = URLInputFile(NO_PHOTO)
        media = InputMediaPhoto(media=photo, caption=product_caption)
        await callback.message.edit_media(media=media, reply_markup=catalog_kb)
    except TelegramBadRequest:
        await callback.message.edit_caption(caption=product_caption, reply_markup=catalog_kb)


@catalog_router.message(Command(commands='catalog'))
async def process_catalog_command(message: Message, bot: Bot, request: Request):
    await request.update_page(page=1, user_id=message.from_user.id)
    product = await request.get_product(0)
    photo_url = product[3]
    product_caption = get_product_caption(product)
    try:
        photo = URLInputFile(photo_url)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=product_caption, reply_markup=catalog_kb)
    except TelegramNetworkError:
        photo = URLInputFile(NO_PHOTO)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=product_caption, reply_markup=catalog_kb)


@catalog_router.callback_query(Text(text=['back']))
async def back_button_press(callback: CallbackQuery, request: Request):
    await request.update_page(page=1, user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.answer()


@catalog_router.callback_query(Text(startswith=['right']))
async def right_button_press(callback: CallbackQuery, request: Request):
    page = await request.get_page(callback.from_user.id)
    catalog_length = await request.get_catalog_length()
    if page < catalog_length:
        product = await request.get_product(page)
        await request.update_page(page=page + 1, user_id=callback.from_user.id)
        await catalog_process(callback, product)
    await callback.answer()


@catalog_router.callback_query(Text(text=['left']))
async def left_button_press(callback: CallbackQuery, request: Request):
    page = await request.get_page(callback.from_user.id)
    if page > 1:
        product = await request.get_product(page - 2)
        await request.update_page(page=page - 1, user_id=callback.from_user.id)
        await catalog_process(callback, product)
    await callback.answer()

# @router.message(Command(commands='load'))
# async def process_load_command(message: Message):
#     data = services.get_data_from_json()
#     database.load_data_in_db(data)
#     await message.answer(text=LEXICON['/load'], reply_markup=None)
