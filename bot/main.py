import asyncio
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from tortoise import Tortoise
from bot import handlers
from aiogram import Bot, Dispatcher
from bot.config import TORTOISE_ORM, config
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # библиотека для уведомлений в телеграм
from dateutil.tz import tzoffset  # библиотека для работы со временем
from bot.middlewares import ApschedulerMiddleware
from aerich import Command


async def start():
    # Logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    logger.info('Starting telegram bot')

    # Bot, Storage, Dispatcher
    logger.info("Bot, Storage, Dispatcher...")
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()  # Сменить на Redis
    dp: Dispatcher = Dispatcher(storage=storage)

    # Обработчик уведомлений
    logger.info("Scheduler...")
    scheduler = AsyncIOScheduler(timezone=tzoffset(None, 5.0 * 3600))
    scheduler.start()
    dp.update.middleware.register(ApschedulerMiddleware(scheduler))

    # Migrations
    logger.info("Migrations...")
    command = Command(tortoise_config=TORTOISE_ORM, location="bot/database/migrations/app", app='app')
    await command.init()
    await command.init_db(safe=True)
    await command.migrate()
    await command.upgrade(run_in_transaction=True)

    # Tortoise-ORM
    logger.info("Tortoise...")
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    # Вносим роутеры в диспетчер
    logger.info("Register handlers...")
    dp.include_router(handlers.base_handlers_router)
    dp.include_router(handlers.catalog_router)
    dp.include_router(handlers.remind_router)
    dp.include_router(handlers.booking_router)
    dp.include_router(handlers.registration_router)

    # Start polling
    try:
        await bot.delete_webhook(True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


# Start telegram bot
if __name__ == "__main__":
    asyncio.run(start())