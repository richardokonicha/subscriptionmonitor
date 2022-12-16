from telethon.sync import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os
import datetime
from config import api_id, api_hash, sessionString, environment, wordpress_url, bot
import logging
import asyncio

# bot_client = TelegramClient('anon', api_id, api_hash)
bot_client = TelegramClient(StringSession(sessionString), api_id, api_hash)




def warnbanTask(userid, username):
    logging.info(f'warn_user from group {username}')
    warn_subscription = description['warn_subscription']
    bot.send_message(userid, text=warn_subscription)
    return True

async def kickTask(userid, channel):
    logging.info(f'kicks user from group {channel}')
    await bot_client.start()
    main_value = await kick(userid, channel)
    answer = main_value['newuser']
    bot.send_message(userid, text=answer)
    print("kicked user lol")
    return main_value

async def unbanTask(user_to_add, channel):
    logging.info(f'Processing task {user_to_add}')
    await bot_client.start()
    main_value = await main(user_to_add, channel)
    return main_value


async def check_group(user_to_add, channel):
    await bot_client.start()
    logging.info(f'Checking group {user_to_add}')
    async for user in bot_client.iter_participants(channel):
        if user_to_add == user.id:
            return True
    return False


async def main(user_to_add, channel_name):
    # checks if user is in a group and add users to channel/ group
    logging.info(f'async add users to channel {user_to_add}')
    await bot_client.start()

    channel = await bot_client.get_entity(channel_name)

    user2 = await bot_client.get_entity('followfootprint')
    user = await bot_client.get_entity(user_to_add)

    check = await check_group(user_to_add, channel)
    if check:
        newuser = f'🟢 Subscription Renewed'
        result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
    else:
        newuser = f'🟢 Congratulations! {channel.title}'
        result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
    return {"channel": channel.title, "newuser": newuser, "userid": user_to_add}


async def kick(userid, channel_name, username):
    logging.info(f'async kick user from channel {userid}')
    await bot_client.start()

    channel = await bot_client.get_entity(channel_name)
    try:
        user = await bot_client.get_entity(userid)
    except:
        user = await bot_client.get_entity(username)

    result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=True)))
    subscription_ended = description['subscription_ended']
    return {"channel": channel.title, "newuser": subscription_ended}

# bot_client.start()
# bot_client.loop.run_until_complete(s
#     main(1205833, channel_name))


# def run_river(user_id):
#     channel_name = int(os.getenv("channel_name"))
#     bot_client.start()
#     main_value = bot_client.loop.run_until_complete(main(user_id, channel_name))
#     return True

def register_user(user_to_add, channel_name):
    value = asyncio.run(main(user_to_add, channel_name))
    print(value)
    return value
