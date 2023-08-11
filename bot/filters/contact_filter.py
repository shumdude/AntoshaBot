from aiogram.filters import BaseFilter
from aiogram.types import Message


class ContactFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        if message.contact is not None:
            return True
        else:
            await message.reply("Пожалуйста, нажмите на кнопку.")
            return False
