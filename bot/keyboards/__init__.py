from aiogram.types import ReplyKeyboardRemove
remove_kb: ReplyKeyboardRemove = ReplyKeyboardRemove()

from .catalog_keyboard import catalog_kb
from .remind_keyboard import create_remind_kb
from .registration_keyboard import contact_kb, remove_kb
from .web_app_keyboard import web_kb
