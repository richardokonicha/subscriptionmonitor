# from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
from telethon.tl.functions.channels import InviteToChannelRequest
import datetime
load_dotenv()
from telethon import TelegramClient, events
from telethon.tl.types import PeerChat, PeerChannel


DEBUG = True
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = "1119377618:AAGr4X08H-VY21yspkgGMTeoqPmo0ulrCuw"
# session_string = os.getenv("Session")

# bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
# 1053579181
# 1205882833
group_name = "https://t.me/testcasechannel"

silver = datetime.timedelta(days=5)
gold = datetime.timedelta(days=10)
# expire_date: "subscription_date" + "subscription_type"

users = {
   852053528: {
      "first_name": "testCase",
      "username": "fcxtextcasebot",
      "id": 852053528,
      "subscription_type": "gold",
      "subscription_date": datetime.datetime(year=2020,month=6, day=4),
      "expire_date": datetime.datetime(year=2020,month=6, day=10),
      "warned": False
   },
   1053579181: {
      "first_name": "Reechee",
      "username": "reechee",
      "id": 1053579181,
      "subscription_type": "silver",
      "subscription_date": datetime.datetime(year=2020,month=6, day=10),
      "expire_date": datetime.datetime(year=2020,month=6, day=12),
      "warned": False
   },
   1205882833: {
      "first_name": "My 4g Glo",
      "username": 'testertestee',
      "id": 1205882833,
      "subscription_type": "silver",
      "subscription_date": datetime.datetime(year=2020,month=6, day=20),
      "expire_date": datetime.datetime(year=2020,month=6, day=30),
      "warned": False

   }
}

# def monitoring():
#    with TelegramClient('session_text', api_id, api_hash) as client:
#       client.send_message(group_name, 'Hello, myself!')

#       # participants_gen = client.iter_participants(group_name)
#       # participants = [i for i in participants_gen]
#       # client.kick_participant(group_name,1205882833)

#       participants = client.get_participants(group_name)
#       now = datetime.datetime.now()
#       warning = datetime.timedelta(days=5)
#       for person in participants:
#          person_id = person.id
#          expire = users[person_id]['expire_date'] 
#          # check if user is registered
#          id_list = users.keys()
#          if person_id in id_list:

#             print(person_id, 'is a user')
#             remain = (expire - now)

#             if remain <= warning:
#                if users[person_id]['warned']==False:
#                   print("he hasn't been warned")
#                   print(f" Your subscription would expire in {remain} please renew before then")
#                   users[person_id]['warned'] = True
#             if expire < now:
#                print("Removing you from channel your subscription has finished please renew")
#             else:
#                print("Your subscription is valid")
               
# monitoring()

      



   # print(client.download_profile_photo(1053579181))

   # @client.on(events.NewMessage(pattern='(?i).*Hello'))
   # async def handler(event):
   #    await event.reply('Hey!')

   # client.run_until_disconnected()


# list_user=list(users.keys())
# def addUser(list_user):
#    client(InviteToChannelRequest(group_name,list_user))


client = TelegramClient('session_text', api_id, api_hash)

@client.on(events.NewMessage)
def my_event_handler(event):
    if 'hello' in event.raw_text:
        event.reply('hi!')

@client.on(events.NewMessage)
async def trooper(event):
    text = event.message.text
    print(text)


# @client.on(events.ChatAction(chats=[-1001313782946]))

@client.on(events.ChatAction(chats=[group_name]))
async def troop(event):
    text = event.message.text
    print(text)


client.start()
client.run_until_disconnected()