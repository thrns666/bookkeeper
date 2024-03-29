from contextlib import asynccontextmanager
from dto import users
from sqlalchemy.orm import Session
from models.users import User
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand, Update
from loguru import logger
import config
import uvicorn
from fastapi import FastAPI, Request
from database import SessionLocal, Base, engine
from routers import user as UserRouter


# DATABASE funcs
def create_user(data: users.User, db: Session):
    user = User(name=data.name)

    try:
        db.add(user)
        db.commit()
        db.refresh()
    except Exception as e:
        print(e)

    return user


def get_user(id: int, db):
    return db.query(User), filter(User.id == id).first()


def update(data: users.User, db: Session, id: int):
    user = db.query(User).filter(User.id==id).first()
    user.name = data.name
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def remove(db: Session, id: int):
    user = db.query(User).filter(User.id==id).first()
    db.commit()
    return user







TOKEN = config.bot_key  # need to change to dotenv (os.getenv(TOKEN_BOT))
WEBHOOK_PATH = f'/bot/{TOKEN}'
WEBHOOK_URL = 'https://70317ba093a291.lhr.life'   # (localhost.run tunnel https url)


# Bot init
# logging.basicConfig(filemode='a', level=logging.INFO, filename='main_log.log')
bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher()


# FastAPI init
@logger.catch
@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    print(webhook_info)

    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
    print('on startup')

    yield

    await bot.session.close()
    print('shutdown')


Base.metaadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)
app.include_router(UserRouter.router, prefix='/user')

# @app.on_event('startup')   # change to lifespan()
# async def on_start_up():
#     webhook_info = await bot.get_webhook_info()
#     print(webhook_info)
#
#     if webhook_info.url != WEBHOOK_URL:
#         await bot.set_webhook(url=WEBHOOK_URL)


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
    # logging.info(f'Start {user_id} {full_user_name} {time.asctime()}. Message: {message}')  # Need change to sql
    # Django drf connect, check user in db
    await message.answer(text='hey start')


@dp.message()
async def default_handler(message: Message):
    try:
        # logging.info(f'Main: {message.from_user.id} {message.from_user.full_name} {time.asctime()}. Message: {message}')
        await message.reply('Default reply on user message')
    except:
        # logging.info(f'Main: {message.from_user.id} {message.from_user.full_name} {time.asctime()}. Message: {message}'
        #              f'. Error in default_handler')
        await message.reply('Something went wrong')


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    tg_update = Update(**update)
    await dp.update(tg_update)


# @app.on_event('shutdown')
# async def on_shutdown():
#     await bot.session.close()


@app.get('/mainnet')
def main_webhandler():
    return {'All': 'good'}


# FastAPI server run
if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
