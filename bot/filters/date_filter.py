from aiogram.filters import BaseFilter
from aiogram.types import Message
from tortoise.fields.data import parse_datetime


class DateFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool | dict:
        try:
            day, month, year = [x for x in message.text.split(".")]
            date = parse_datetime(f"{year}-{month}-{day}").date()
            return {'date': date}
        except ValueError:
            await message.reply("Неверный формат или некорректная дата.")
            return False
