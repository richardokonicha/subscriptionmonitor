from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
load_dotenv()
from helpers import schedule_renew
from config import scheduler

api_hash = os.getenv("api_hash")
api_id = os.getenv("api_id")
sessionString = os.getenv("sessionString")


# import database as db
# scheduler.start()


# objects = db.User.objects.all()

# for bst_user in objects:
#     add = schedule_renew(bst_user)
#     print(bst_user)

# print(objects)


client = TelegramClient(StringSession(''), api_id, api_hash)




async def main(userid, channel_name, username):
    me = await client.get_me()

    # You can print all the dialogs/conversations that you are part of:
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)

    user = userid
    try:
        await client.connect()
        channel = await client.get_entity(channel_name)
        user = await client.get_entity(userid)
    except:
        user = await client.get_entity(username)

    try:
        msg = "grant"
        # result = await client.edit_permissions(channel, user, view_messages=True)
        print('Grant user', channel.id, user.id)
        result = await client(
            # revoke_access
            EditBannedRequest(
                channel.id, user.id, ChatBannedRights(
                    until_date=None, view_messages=True)
            )

            # grant_access
            # EditBannedRequest(
            #     channel.id,
            #     user.id,
            #     ChatBannedRights(until_date=None, view_messages=False),
            # )
        )
    except Exception as e:
        print(e)

    await client.disconnect()
    return user

with client:
    userid = 1053579181
    username = 'followfootprint'
    channel_name = -1001293337449
    client.loop.run_until_complete(main(userid, channel_name, username))