from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_remind_kb(job_id: str) -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Выполнено',
        callback_data='y_' + job_id)
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Не сделано',
        callback_data='n_' + job_id)
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard
