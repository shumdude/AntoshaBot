import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator
from bot import handlers
from bot.config import TORTOISE_ORM, config
from bot.middlewares import ApschedulerMiddleware, TranslatorRunnerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dateutil.tz import tzoffset
from tortoise import Tortoise
from aerich import Command


async def start():
    # Logging: Structlog как вариант
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

    # Обработчик уведомлений: taskiq как вариант
    logger.info("Scheduler...")
    scheduler = AsyncIOScheduler(timezone=tzoffset(None, 5.0 * 3600))
    scheduler.start()
    dp.update.middleware.register(ApschedulerMiddleware(scheduler))

    # Fluentogram
    logger.info("Fluentogram...")
    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en",)
        },
        [
            FluentTranslator("ru", translator=FluentBundle.from_files("ru", ["bot/locales/ru.ftl"])),
            FluentTranslator("en", translator=FluentBundle.from_files("en-US", ["bot/locales/en.ftl"]))
        ])
    dp.callback_query.middleware.register(TranslatorRunnerMiddleware())
    dp.message.middleware.register(TranslatorRunnerMiddleware())

    # Tortoise-ORM: SQLAlchemy как вариант
    logger.info("Tortoise init...")
    await Tortoise.init(config=TORTOISE_ORM)
    logger.info("Tortoise generate schemas...")
    await Tortoise.generate_schemas()

    # Migrations: alembic как вариант
    logger.info("Migrations...")
    command = Command(tortoise_config=TORTOISE_ORM, location="bot/database/migrations", app='app')
    logger.info("Init...")
    await command.init()
    # logger.info("Init DB...")
    # await command.init_db(safe=True)
    logger.info("Migrate...")
    await command.migrate()
    logger.info("Upgrade...")
    await command.upgrade(run_in_transaction=True)

    # Вносим роутеры в диспетчер
    logger.info("Register handlers...")
    dp.include_router(handlers.base_handlers_router)
    dp.include_router(handlers.catalog_router)
    dp.include_router(handlers.remind_router)
    dp.include_router(handlers.booking_router)
    dp.include_router(handlers.registration_router)
    dp.include_router(handlers.qrcode_router)
    # dp.include_router(handlers.web_app_router)

    # Start polling
    try:
        await bot.delete_webhook(True)
        await dp.start_polling(bot, _translator_hub=translator_hub)
    finally:
        await bot.session.close()


# Start telegram bot
if __name__ == "__main__":
    asyncio.run(start())
