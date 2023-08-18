from path import Path
from bot.services import generate_qr_code
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, File

qrcode_router: Router = Router()  # Инициализируем роутер уровня модуля


@qrcode_router.message(Command(commands='qrcode'))
async def process_commands_command(message: Message, bot: Bot):
    text = f"@{message.from_user.username}\n\n" \
           f"{message.from_user.first_name}, {message.from_user.last_name}\n\n" \
           f"{message.from_user.id}"
    profile_photos = await message.from_user.get_profile_photos()
    file: File = await bot.get_file(file_id=profile_photos.photos[0][0].file_id)
    await bot.download_file(file_path=file.file_path, destination=f"bot/services/example_{message.from_user.id}.jpg")
    path_to_download = Path().joinpath("bot/services", "example.jpg")
    path_to_save = Path().joinpath("bot/services", "example.png")
    generate_qr_code(text, path_to_download, path_to_save)
    photo = FSInputFile("bot/services/example.png")
    await bot.send_photo(message.from_user.id, photo)



