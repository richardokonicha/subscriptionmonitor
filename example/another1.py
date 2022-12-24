# from telethon import TelegramClient
import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession


api_id='1347918'
api_hash='5681581438678d9390cd4f67ee764f82'
# sessionString='1BJWap1wBuxArH3y6QjWYuOaQz -VeeJWmzvtb4FteQ62TfVdoolz9nDRA-BYMpGFYikb5KQbP4ziiBj8jCcIj2A0fen1utpfi7o3SU2rkHgioWhvtpI_GxrN5R7JLRa4yM6clGshFHKHWAB-qGCtPJdyeodvbCdvjXI_zKlRl_BuJxADeHN_v-npwV9Iisor5yi3Zy_r7QyHguGpw-oOFVuyCqEJe1lfLUtb1e_wJOMCk6-K_dgq_y7bfl-s54z6PjubOCL7CUb8xCVVsq37YDJbsRgwKRHvsiSKQDpCWS4qXCNR_uSRKTWfjEWP4_5T6xWvaldZeyN2_SuZZcmzT6fA2E7iM5DA='

class MyClient:
  def __init__(self):
    self.client = TelegramClient('StringSession(sessionString)', api_id, api_hash)
    self.client.start()

# client = MyClient()
client = TelegramClient('StringSession(sessionString)', api_id, api_hash)


async def check_group(user_to_add, channel):
    # logging.info(f'Checking group {user_to_add}')
    # await bot_client.start()
    await client.start()

    async for dialog in client.iter_dialogs():
        print(dialog.name)
    return True


async def sleep_async(seconds):
    await asyncio.sleep(seconds)
    print("Woke up after {} seconds".format(seconds))

# You can then run this function using asyncio.run()

print('my name is paul')
valu = asyncio.run(check_group('fugoku', 'followfootprint'))
print(valu)
print('my name john')
# class MyClient:
#   def __init__(self):
#     self.client = TelegramClient('StringSession(sessionString)', api_id, api_hash)
#     self.client.start()

#   def send_message(self, message, recipient):
#     self.client.send_message('me', "hello, world sync")

#   async def get_dialogs(self):
#     # with TelegramClient(StringSession(sessionString), api_id, api_hash) as client:
#     async for dialog in self.bot_client.iter_dialogs():
#         print(dialog.name)

#   # def some_sync_function(self):
#   #   loop = asyncio.new_event_loop()
#   #   asyncio.set_event_loop(loop)
#   #   loop.run_until_complete(self.get_dialogs())
#     def some_sync_function(self):
#       asyncio.run(self.get_dialogs())

    



# client = MyClient()

# client.some_sync_function()
# print('fsdfds')

# # async def async_send_message():
# #   await client.client.send_message('me', "hello, world async")




# # asyncio.run(async_send_message())

# from telethon.tl.functions.messages import SendReactionRequest


# await client(SendReactionRequest(
#     peer=chat,
#     msg_id=42,
#     reaction='❤️'
# ))
