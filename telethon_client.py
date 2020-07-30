from telethon.sync import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest , InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
phone = '+2349050556321'
userid= 1053579181
user_to_add =1205882833
subscription=datetime.datetime(2020, 9, 11, 16)

# bot = TelegramClient('anon', api_id, api_hash)
bot = TelegramClient('anon', 1347918, '5681581438678d9390cd4f67ee764f82')
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     client.sign_in(phone, input("Enter code"))
# bot = TelegramClient('bot', api_id,  api_hash).start(bot_token='1261225499:AAFBWIrd2oCKH4FarmRl-w1R9tW2Q-xxG9E')
channel_id = '-1001313782946'
channel_name = 'testcasechannel'

async def check_group(user_to_add):
    # checks group if user is already participant
    channel = await bot.get_entity(channel_name)
    async for user in bot.iter_participants(channel):
        if user_to_add == user.id:
            return True
    return False

async def main(user_to_add):
    # checks if user is in a group and add users to channel/ group
    channel = await bot.get_entity(channel_name)
    check = await check_group(user_to_add)
    if check:
        await bot.send_message(user_to_add, f'Your subscription has been renewed on {channel.title}')
    else:
        result = await bot(InviteToChannelRequest(channel.id,[user_to_add]))
        await bot.send_message(user_to_add, f'Welcome to {channel.title}')


async def kick(user_to_add):
    # kicks users out of group
    channel = await bot.get_entity(channel_name)
    result = await bot(EditBannedRequest(channel.id, user_to_add, ChatBannedRights(until_date=None,view_messages=True)))
    await bot.send_message(user_to_add, f'Youve bee kicked out of {channel.title}')


# bot.start()
# bot.loop.run_until_complete(kick(1205882833))





