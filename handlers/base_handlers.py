from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from settings import LEXICON
from database import Request

base_handlers_router: Router = Router()  # Инициализируем роутер уровня модуля


@base_handlers_router.message(CommandStart())
async def process_start_command(message: Message, request: Request, bot: Bot):
    await request.add_user(message.from_user.id)
    sent_message: Message = await message.answer(text=LEXICON['/start'])
    await bot.unpin_all_chat_messages(message.chat.id)
    await sent_message.pin()


@base_handlers_router.message(Command(commands='commands'))
async def process_commands_command(message: Message):
    await message.answer(text=LEXICON['/commands'])

# @base_handlers_router.message(Command(commands='test'))
# async def test(message: Message, bot: Bot, scheduler: AsyncIOScheduler):
#     await bot.send_message(message.chat.id, 'add job . . .')
#     scheduler.add_job(apscheduler_def, trigger='date', run_date=datetime.now() + timedelta(seconds=5),
#                       args=(message, bot))
# @base_handlers_router.message(Command(commands='both'))
# async def process_add_user(message: Message, bot: Bot, scheduler: AsyncIOScheduler, request: Request):
#     await request.add_datauser(message.from_user.id, message.from_user.username)
#     await bot.send_message(message.chat.id, 'add_user')
# async def apscheduler_def(message: Message, bot: Bot):
#     await bot.send_message(message.chat.id, 'complete ! ! !')
