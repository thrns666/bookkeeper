from aiogram.types import Message
# import from drf db for user_data(first_name, id, etc...)


def hello(user_id: Message.from_user.id, user_firstname: Message.from_user.first_name):

    start_text = f'Hello [user_firstname], ur id is [user_id] successfully login, nice to meet u.'
    return start_text
