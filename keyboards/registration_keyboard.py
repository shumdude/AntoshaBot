from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

buttons = []
contact_button: KeyboardButton = KeyboardButton(text="Поделиться номером телефона", request_contact=True)
buttons.append(contact_button)
contact_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[buttons])
remove_kb: ReplyKeyboardRemove = ReplyKeyboardRemove()
