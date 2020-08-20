from telethon.sync import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os
import datetime
from config import api_id, api_hash, sessionString


# bot_client = TelegramClient('anon', api_id, api_hash)
bot_client = TelegramClient(
    StringSession(sessionString), api_id, api_hash)


async def check_group(user_to_add, channel):
    # checks group if user is already participant
    # channel = await bot_client.get_entity(channel_name)
    async for user in bot_client.iter_participants(channel):
        if user_to_add == user.id:
            return True
    return False


async def main(user_to_add, channel_name):
    # checks if user is in a group and add users to channel/ group
    channel = await bot_client.get_entity(channel_name)
    dialogs = await bot_client.get_dialogs()
    user = await bot_client.get_entity(user_to_add)

    check = await check_group(user_to_add, channel)
    if check:
        newuser = f'🟢 Subscription Renewed'
        result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
    else:
        newuser = f'🟢 Congratulations! {channel.title}'
        # result = await bot_client(InviteToChannelRequest(channel.id, [user_to_add]))
        result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))

    return {"channel": channel.title, "newuser": newuser}


async def kick(user_to_add, channel_name):
    # kicks users out of group
    # TestChannelBst = -1001476945873
    # dialogs = await bot_client.get_dialogs()
    channel = await bot_client.get_entity(channel_name)
    user = await bot_client.get_entity(user_to_add)

    result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=True)))
    newuser = f"""
    
🔴 Your subscription has ended Renew it to have access VIP

Www.bst-forexgroup.com

Info @bsttrading 

BsTTeam
    """
    return {"channel": channel.title, "newuser": newuser}

# bot_client.start()
# bot_client.loop.run_until_complete(
#     main(1205833, channel_name))
