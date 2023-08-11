from aiogram import Bot, Dispatcher
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)


class GoodsCallbackFactory(CallbackData, prefix='goods', sep='|'):
    category_id: int
    subcategory_id: int
    item_id: int


button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Категория 1',
    callback_data=GoodsCallbackFactory(
        category_id=1,
        subcategory_id=0,
        item_id=0).pack())

button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='Категория 2',
    callback_data=GoodsCallbackFactory(
        category_id=2,
        subcategory_id=0,
        item_id=0).pack())

markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
