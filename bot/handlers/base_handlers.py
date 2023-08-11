from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bot.settings import LEXICON
from bot.database.db_requests import add_user

base_handlers_router: Router = Router()  # Инициализируем роутер уровня модуля


@base_handlers_router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    await add_user(message.from_user.id)
    sent_message: Message = await message.answer(text=LEXICON['/start'])
    await bot.unpin_all_chat_messages(message.chat.id)
    await sent_message.pin()


@base_handlers_router.message(Command(commands='commands'))
async def process_commands_command(message: Message):
    await message.answer(text=LEXICON['/commands'])
