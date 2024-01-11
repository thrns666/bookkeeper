from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
import config
from bot.ops import hello

# Bot init

bot: Bot = config.bot_key
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
    # Django drf connect, check user in db
    await message.answer(text=hello(user_id=message.from_user.id, user_firstname=message.from_user.first_name))


