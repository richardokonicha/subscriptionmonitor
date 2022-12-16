import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os
import datetime
from config import api_id, api_hash, sessionString, environment, wordpress_url
import logging
from interface import add_to_queue
# from telethon_client import TeleFacade

# bot_client = TelegramClient('anon', api_id, api_hash)
# bot_client = TelegramClient(StringSession(sessionString), api_id, api_hash)
class TeleFacade():
    bot_client = TelegramClient(StringSession(sessionString), api_id, api_hash)
    print('inner1 ')
    def __init__(self):
        self.bot_client.start()
        print('init 2 ')


    def get_user(self):
        print('iiniit 2')
        # with TelegramClient(StringSession(sessionString), api_id, api_hash) as client:
        user = self.bot_client.get_me().username
        print(user)
        return user

    def add(self):
        return True

    def __str__(self):
        return self.get_user()

def check_group_sync(user_to_add, channel):
    logging.info(f'Checking group {user_to_add} kjjkjkjkjk')

    with TelegramClient(StringSession(StringSession(sessionString)), api_id, api_hash) as client:
        print(client.get_me().username)

        message = client.send_message('me', 'Hi!')

        return


async def check_group(user_to_add, channel):
    logging.info(f'Checking group {user_to_add}')
    await bot_client.start()


    async for user in bot_client.iter_participants(channel):
        if user_to_add == user.id:
            return True
    return False

def execute_background_task(batch_num):
    print("Batch number is ", batch_num)
    # lord = TeleFacade()
    
    # print(user.get_user())
    # lord.add(userid)
    # do stuff
    time.sleep(30)
    return True


def testLord():
    print("Batch number is ")
    lord = TeleFacade()
    print(lord.get_user())
    # lord.add(userid)
    # time.sleep(30)
    return True



def queueChat():
    job = add_to_queue(testLord)
    print('added')

    return job.get_id()


# testLord()
