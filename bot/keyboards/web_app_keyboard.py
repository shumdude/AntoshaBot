from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

web_button = KeyboardButton(text='WebApp', web_app=WebAppInfo(url="https://shumdude.github.io/antosha-pages/"))
buttons = [[web_button]]
web_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

