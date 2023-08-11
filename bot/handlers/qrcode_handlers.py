from path import Path
from bot.services import gen_qr_code
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

qrcode_router: Router = Router()  # Инициализируем роутер уровня модуля


@qrcode_router.message(Command(commands='qrcode'))
async def process_commands_command(message: Message, bot: Bot):
    text = "Ха-ха-ха, смотри, я - QR-код!"
    path_to_download = Path().joinpath("bot/services", "example.jpeg")
    path_to_save = Path().joinpath("bot/services", "example.png")
    gen_qr_code(text, path_to_download, path_to_save)
    photo = FSInputFile("bot/services/example.png")
    await bot.send_photo(message.from_user.id, photo)


