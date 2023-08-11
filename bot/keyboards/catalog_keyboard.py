from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.settings import LEXICON

# Catalog keyboard
left_button: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON['left'], callback_data='left')
right_button: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON['right'], callback_data='right')
back_to_menu_button: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON['back'], callback_data='back')
# page_button: InlineKeyboardButton = InlineKeyboardButton(text='Страницы', callback_data='page')
buttons: list[InlineKeyboardButton] = [left_button, right_button, back_to_menu_button]
catalog_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
catalog_kb_builder.row(*buttons, width=2)
catalog_kb: InlineKeyboardMarkup = catalog_kb_builder.as_markup()
