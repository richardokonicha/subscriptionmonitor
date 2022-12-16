# from interface import add_to_queue
# from telethon.sync import TelegramClient
# from telethon.sessions import StringSession

# api_id='1347918'
# api_hash='5681581438678d9390cd4f67ee764f82'
# sessionString='1BJWap1wBuxArH3y6QjWYuOaQz-VeeJWmzvtb4FteQ62TfVdoolz9nDRA-BYMpGFYikb5KQbP4ziiBj8jCcIj2A0fen1utpfi7o3SU2rkHgioWhvtpI_GxrN5R7JLRa4yM6clGshFHKHWAB-qGCtPJdyeodvbCdvjXI_zKlRl_BuJxADeHN_v-npwV9Iisor5yi3Zy_r7QyHguGpw-oOFVuyCqEJe1lfLUtb1e_wJOMCk6-K_dgq_y7bfl-s54z6PjubOCL7CUb8xCVVsq37YDJbsRgwKRHvsiSKQDpCWS4qXCNR_uSRKTWfjEWP4_5T6xWvaldZeyN2_SuZZcmzT6fA2E7iM5DA='

# import requests

# def count_words_at_url(url):
#     resp = requests.get(url)
#     return

from rq import Queue
from redis import from_url
redis_conn = from_url('redis://default:redispw@localhost:55000/6')
q = Queue(connection=redis_conn)



# class TeleFacade():
#     bot_client = TelegramClient(StringSession(sessionString), api_id, api_hash)

#     def __init__(self):
#         self.bot_client.start()

#     def get_user(self):
#         # with TelegramClient(StringSession(sessionString), api_id, api_hash) as client:
#         user = self.bot_client.get_me().username
#         print(user)
#         return user

#     def add(self):
#         return True

def testLord():
    print("Batch number is 77")
    # lord = TeleFacade()
    # user = lord.get_user()
    # print(user)
    return True

# # def queueTest():
# #     print('did you check')

# #     return 

# # def queueChat():
# #     job = q.enqueue(queueTest)
  
# #     # job = add_to_queue(queueTest)
# #     print('added')

# #     return



# # # queueChat()
from task1 import testLord
from datetime import datetime
now = datetime.now()
print(now, 'j')

def rt():
  print('klkj')
  return True

from task1 import rt

job = q.enqueue(rt)
# print(job)