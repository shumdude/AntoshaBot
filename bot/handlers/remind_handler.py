from datetime import datetime, timedelta
from aiogram.filters import Text, Command, StateFilter
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fluentogram import TranslatorRunner
from bot.database.db_requests import add_data, get_sender
from bot.states import FSMRemind
from bot.keyboards import create_remind_kb

remind_router: Router = Router()  # Инициализируем роутер уровня модуля


# Отмена
@remind_router.message(Command(commands='cancel_remind'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await message.answer(i18n.remind.cancel())
    await state.clear()


# Точка входа - remind
@remind_router.message(Command(commands='remind'), StateFilter(default_state))
async def process_fsm_command(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await message.answer(i18n.remind.start())
    await state.set_state(FSMRemind.telegram_id)


# ТелеграмИд
@remind_router.message(StateFilter(FSMRemind.telegram_id))
async def process_tel_id(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await state.update_data(telegram_id=message.text)
    await message.answer(i18n.remind.test())
    await state.set_state(FSMRemind.test)


# Тест
@remind_router.message(StateFilter(FSMRemind.test))
async def process_test(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await state.update_data(test=message.text)
    await message.answer(i18n.remind.date())
    await state.set_state(FSMRemind.date)


# Дата
@remind_router.message(StateFilter(FSMRemind.date))
async def process_date(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await state.update_data(date=message.text)
    await message.answer(i18n.remind.time())
    await state.set_state(FSMRemind.time)


# Время
@remind_router.message(StateFilter(FSMRemind.time))
async def process_time(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await state.update_data(time=message.text)
    await message.answer(i18n.remind.answer_time())
    await state.set_state(FSMRemind.answer_time)


# Точка выхода - answer_time
@remind_router.message(StateFilter(FSMRemind.answer_time))
async def process_answer_time(message: Message, state: FSMContext, bot: Bot,
                              scheduler: AsyncIOScheduler, i18n: TranslatorRunner):
    await state.update_data(answer_time=message.text)
    data = await state.get_data()
    job: Job = scheduler.add_job(if_ignore,
                                 trigger='date',
                                 run_date=datetime.now() + timedelta(seconds=int(data["answer_time"])),
                                 args=(message, bot, i18n))
    job_kb = await create_remind_kb(job.id)  # создаём клавиатуру для данного job
    await add_data(message.from_user.id,
                   int(data["telegram_id"]),
                   data["test"],
                   data["date"],
                   data["time"],
                   int(data["answer_time"]),
                   job.id)
    """Нужно добавить обработку исключений для answer_time, telegram_id и отправки сообщения пользователю"""
    await state.clear()
    await bot.send_message(chat_id=data["telegram_id"],
                           text=i18n.remind.job(id=message.from_user.id,
                                                test=data['test'],
                                                date=data['date'],
                                                time=data['time'],
                                                answer_time=data['answer_time']),
                           reply_markup=job_kb)
    await message.answer(text="Готово. Отправили напоминание пользователю.")


# Если пользователь не нажал на кнопку
async def if_ignore(message: Message, bot: Bot, i18n: TranslatorRunner):
    await bot.send_message(message.chat.id, i18n.remind.ignore())


# Выполнено
@remind_router.callback_query(Text(startswith=['y_']))
async def process_done_press(callback: CallbackQuery, scheduler: AsyncIOScheduler, bot: Bot, i18n: TranslatorRunner):
    job_id = await job_remove(callback, scheduler)
    sender_id = await get_sender(job_id)
    await bot.send_message(chat_id=sender_id,
                           text=i18n.remind.press.done(username=callback.from_user.username,
                                                       user_id=callback.from_user.id))
    await process_remind_press(callback, i18n.remind.done())


# Не сделано
@remind_router.callback_query(Text(startswith=['n_']))
async def process_not_done_press(callback: CallbackQuery, scheduler: AsyncIOScheduler, bot: Bot,
                                 i18n: TranslatorRunner):
    job_id = await job_remove(callback, scheduler)
    sender_id = await get_sender(job_id)
    await bot.send_message(chat_id=sender_id,
                           text=i18n.remind.press.not_done(username=callback.from_user.username,
                                                    user_id=callback.from_user.id))
    await process_remind_press(callback, i18n.remind.not_done())


# Нажата кнопка клавиатуры job
async def process_remind_press(callback: CallbackQuery, text: str):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(text=text, reply_markup=None)


async def job_remove(callback: CallbackQuery, scheduler: AsyncIOScheduler) -> str:
    job_id: str = callback.data.split("_")[-1]
    job: Job = scheduler.get_job(job_id=job_id)
    job.remove()
    return job_id
