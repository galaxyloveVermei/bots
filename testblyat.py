import logging
import time
from telebot import types
from lightdb import LightDB
from aiogram.utils.executor import start_polling
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = '6654870459:AAHXKJNMouotHFhInIZPZcFkZTDQERD4BuA'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = LightDB('users.json') 
init_ts = time.perf_counter()
admins = ["6508245262"]

class States(StatesGroup):
    waiting_for_msg = State()

def uptime():
    uptime = round(time.perf_counter() - init_ts)
    return uptime

@dp.message_handler(commands=["start"], state=None)
async def cmd_start(message: types.Message):
    await message.reply("Привет!\n"
                        ""
                        ""
                        ""
                        )
    try:
        users: list = db.get('users')
        if message.from_user.id not in users:
            users.append(message.from_user.id)
            db.set('users', users)
    except:
        users = []
        users.append(message.from_user.id)
        db.set('users', users)
 
@dp.message_handler(commands=["donate"])
async def donate(message:types.message):
    await message.answer(
        ""
    )

@dp.message_handler(commands=["help"])
async def help(message: types.message):
    await message.answer(
        "/ping - показывает пинг бота\n"
        "/help - показать это смс\n"
        "/start - стартовое смс\n"
    )

@dp.message_handler(commands=["ping"])
async def ping_handler(message: types.Message):
        start_time = time.time()
        await message.answer('🏓 Понг!')
        end_time = time.time()
        duration_ms = int(round((end_time - start_time) * 1000))
        await message.answer(f'⏱️ Пинг: <code>{duration_ms}</code> ms\n⏳ Аптайм: <code>{uptime()}</code>')
        
@dp.message_handler(commands=['send'])
async def send_messages(message: types.Message):
    if message.from_user.id not in admins:
        await message.answer('This command not for you')
        return
    await message.answer('<b>Введите сообщение для рассылки</b>')
    await States.waiting_for_msg.set()

@dp.message_handler(state=States.waiting_for_msg)
async def sending(message: types.Message):
    usrs: list = db.get('users')
    user_sec = []
    user_not = []
    for i in usrs:
        try:
            await dp.bot.send_message(i, message.text)
            user_sec.append(i)
        except:
            user_not.append(i)
    await message.answer(f'<b>Рассылка успешно завершена. Сообщения успешно отправлены {len(user_sec)} людям\nНе отправлено {len(user_not)}</b>')
    await States.next()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
