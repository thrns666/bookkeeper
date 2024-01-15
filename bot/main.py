from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand, Update
import config
import uvicorn
from fastapi import FastAPI, Request
import time
import os
import logging
from bot.ops import hello

# FastAPI init

app = FastAPI()

TOKEN = config.bot_key  # need to change to dotenv (os.getenv(TOKEN_BOT))
WEBHOOK_PATH = f'/bot/{TOKEN}'  # mb away out
RENDER_WEBSERVICE_NAME = '<MY_RENDER_SERVICE>'  # i dont get it
WEBHOOK_URL = 'https://' + RENDER_WEBSERVICE_NAME + 'onrender.com' + WEBHOOK_PATH   # (localhost.run tunnel https url)


@app.on_event('startup')
async def on_start_up():
    webhook_info = await bot.get_webhook_info()
    print(webhook_info)

    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

# Bot init

logging.basicConfig(filemode='a', level=logging.INFO)
bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher(Bot)


# Filters for ex('+', '-')
def counting_filter(message: Message) -> bool:
    return True if message.text.startswith(('+', '-')) else False


# Menu button
async def menu_button(bot: Bot):
    menu_commands = [
        BotCommand(command='/balance', description=''),
        BotCommand(command='/add', description='')
    ]
    await bot.set_my_commands(menu_commands)


# Handlers
@dp.message(CommandStart())
async def command_start(message: Message):
    user_id = message.from_user.id
    full_user_name = message.from_user.full_name
    logging.info(f'Start {user_id} {full_user_name} {time.asctime()}. Message: {message}')  # Need change to sql
    # Django drf connect, check user in db
    await message.answer(text=hello(user_id=user_id, user_firstname=full_user_name))


@dp.message()
async def default_handler(message: Message):
    try:
        logging.info(f'Main: {message.from_user.id} {message.from_user.full_name} {time.asctime()}. Message: {message}')
        await message.reply('Default reply on user message')
    except:
        logging.info(f'Main: {message.from_user.id} {message.from_user.full_name} {time.asctime()}. Message: {message}'
                     f'. Error in default_handler')
        await message.reply('Something went wrong')


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    tg_update = Update(**update)
    await dp.update(tg_update)


@app.on_event('shutdown')
async def on_shutdown():
    await bot.session.close()


@app.get('/')
def main_webhandler():
    return {'All': 'good'}


# FastAPI server run

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
