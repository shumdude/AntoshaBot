import asyncio
import logging
import asyncpg
from aiogram.fsm.storage.memory import MemoryStorage
import handlers
from aiogram import Bot, Dispatcher
from config import Config, load_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # библиотека для уведомлений в телеграм
from dateutil.tz import tzoffset  # библиотека для работы со временем
from middlewares import ApschedulerMiddleware, DatabaseMiddleware


# Function to create pool with database
async def create_pool(config: Config) -> asyncpg.pool.Pool:
    return await asyncpg.create_pool(user=config.db.db_user,
                                     password=config.db.db_password,
                                     host=config.db.db_host,
                                     database=config.db.database)


async def start():
    # Logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    logger.info('Starting telegram bot')

    # Config, Bot, Dispatcher
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # DatabaseMiddleware
    pool_connect = await create_pool(config)
    dp.update.middleware.register(DatabaseMiddleware(pool_connect))

    # Обработчик уведомлений
    scheduler = AsyncIOScheduler(timezone=tzoffset(None, 5.0 * 3600))
    scheduler.start()
    dp.update.middleware.register(ApschedulerMiddleware(scheduler))

    # Вносим роутеры в диспетчер
    dp.include_router(handlers.base_handlers_router)
    dp.include_router(handlers.catalog_router)
    dp.include_router(handlers.remind_router)

    # Start polling
    try:
        await bot.delete_webhook(True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


# Start telegram bot
if __name__ == "__main__":
    asyncio.run(start())
