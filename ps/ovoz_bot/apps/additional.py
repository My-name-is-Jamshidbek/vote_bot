import random
from database import *
from loader import bot, dp


def generate_random_numbers():
    random_numbers = ""
    for _ in range(4):
        random_numbers+=str(random.randint(1, 10))
    return random_numbers

async def check_join(user_id):
    try:
        for i in read_channels():
            member = await bot.get_chat_member(chat_id=i["link"], user_id=user_id)
            if member["status"] == "left": return False
        return True
    except Exception as e:
        print(e)
        return False

async def check_join_a(user_id, channel_id):
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member["status"] == "left": return False
        return True
    except Exception as e:
        print(e)
        return False
