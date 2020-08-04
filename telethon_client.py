from telethon.sync import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
sessionString = os.getenv("sessionString")

# bot_client = TelegramClient('anon', api_id, api_hash)
# bot_client = TelegramClient(
#     'anon', 1347918, '5681581438678d9390cd4f67ee764f82')
# sessionString = StringSession.save(bot_client.session)

bot_client = TelegramClient(
    StringSession(sessionString), api_id, api_hash)

# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     client.sign_in(phone, input("Enter code"))
# bot_client = TelegramClient('bot_client', api_id,  api_hash).start(bot__client_token='1261225499:AAFBWIrd2oCKH4FarmRl-w1R9tW2Q-xxG9E')
channel_name = 'testcasechannel'


async def check_group(user_to_add):
    # checks group if user is already participant
    channel = await bot_client.get_entity(channel_name)
    async for user in bot_client.iter_participants(channel):
        if user_to_add == user.id:
            return True
    return False


async def main(user_to_add):
    # checks if user is in a group and add users to channel/ group
    channel = await bot_client.get_entity(channel_name)
    check = await check_group(user_to_add)
    if check:
        newuser = f'🟢Congratulations! Your subscription has been renewed on {channel.title}🟢'
        # await bot_client.send_message(user_to_add, f'Your subscription has been renewed on {channel.title}')
    else:
        newuser = f'🟢Congratulations! Welcome to {channel.title}🟢'
        result = await bot_client(InviteToChannelRequest(channel.id, [user_to_add]))
        # await bot_client.send_message(user_to_add, f'Welcome to {channel.title}')

    return {"channel": channel.title, "newuser": newuser}


async def kick(user_to_add):
    # kicks users out of group
    channel = await bot_client.get_entity(channel_name)
    result = await bot_client(EditBannedRequest(channel.id, user_to_add, ChatBannedRights(until_date=None, view_messages=True)))
    # await bot_client.send_message(user_to_add, f'Youve bee kicked out of {channel.title}')
    newuser = f"🔴Sorry you've been kicked out from {channel.title}🔴"
    return {"channel": channel.title, "newuser": newuser}


# bot_client.start()
# bot_client.loop.run_until_complete(kick(1205882833))
