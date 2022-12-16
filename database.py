import datetime
from mongoengine import *
from mongoengine import connect
from dotenv import load_dotenv
import telebot
import os
from telethon_client import main, kick, unbanTask, warnbanTask, kickTask, register_user
from config import scheduler, bot, wordpress_url, environment, bot_client
import logging
from interface import add_to_queue, report_success, report_failure, q
import asyncio

from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

load_dotenv()

db_host = os.getenv('db_host')

connect('monitor_db', host=db_host)


# async def check_group(user_to_add, channel):
#     await bot_client.start()
#     logging.info(f'Checking group {user_to_add}')
#     async for user in bot_client.iter_participants(channel):
#         if user_to_add == user.id:
#             return True
#     return False

async def sleep_async(seconds):
    await asyncio.sleep(seconds)
    print("Woke up after {} seconds".format(seconds))

# async def main(user, channel_name):
#     # checks if user is in a group and add users to channel/ group

#     userid = user.userid
#     username = user.username

#     logging.info(f'async add users to channel {username}')

#     await bot_client.start()

#     channel = await bot_client.get_entity(channel_name)

#     # user2 = await bot_client.get_entity('followfootprint')

#     try:
#         print('fetching user by id')
#         user = await bot_client.get_entity(userid)
#     except Exception as e:
#         print('fetching user by username', e)
#         user = await bot_client.get_entity(username)
#     # except:
#     #     print('couldnt get this user')
#     else:
#         print("Everything is ok.")

            

#     try:
#         check = await check_group(userid, channel)

#         if check:
#             msg = f'🟢 Subscription Renewed'
#             result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
#         else:
#             msg = f'🟢 Congratulations! {channel.title}'
#             result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))

#     except Exception as e:
#         print("An error occurred!", e)
#         return 

#     value = {"channel": channel.title, "msg": msg, "user": {'userid': userid, 'username': username}}
#     return value



class User(Document):
    # user object
    userid = IntField(unique=True)
    username = StringField()
    subscriptionstatus = StringField()  # subscribed or unsubscribed
    orders = ListField(IntField())
    subscription = DateTimeField(default=datetime.datetime.utcnow())

    def checksub(self):
        logging.info('Checking sub')

        if bool(self.subscription) == False:
            return False
        else:
            if self.subscription <= datetime.datetime.utcnow():
                return False
            else:
                return self.subscription - datetime.datetime.utcnow()

    def addsubscription(self, subscribed_time):
        logging.info('addsubscription ')

        sub = self.checksub()
        if sub == False:
            self.subscription = datetime.datetime.utcnow() + subscribed_time
            self.save()
            return self.subscription
        else:
            self.subscription = self.subscription + subscribed_time
            self.save()
            return self.subscription

    def subscribed_to(self, productid, orderid):
        print(productid, orderid, "product id and orderid respectively")
        # self.orders.append(orderid)
        if productid == 101010:
            subscribed_time = datetime.timedelta(minutes=1)

        if productid == 978:
            # 1 month subscription
            subscribed_time = datetime.timedelta(days=30)

        if productid == 979:
            # 2 months subscription
            subscribed_time = datetime.timedelta(days=60)

        if productid == 980:
            # 1 year subscription
            subscribed_time = datetime.timedelta(days=365)

        if productid == 25:
            # 1 year subscription
            subscribed_time = datetime.timedelta(weeks=4000)
        
        if subscribed_time:
            subscription = self.addsubscription(subscribed_time)
            # job = self.set_user_bst()
        else:
            print("subscribed time is null")
        return subscription

    # def kick_user(self):
    #     # kicks user from group
    #     logging.info(f'kicks user from group {self.username}')

    #     userid = self.userid
    #     username = self.username
    #     channel_name = int(os.getenv("channel_name"))
    #     bot_client.start()
    #     main_value = bot_client.loop.run_until_complete(
    #         kick(userid, channel_name))

    #     answer = main_value['newuser']
    #     bot.send_message(userid, text=answer)
    #     print("kicked user lol")

#     def warn_user(self):
#         # kicks user from group
#         logging.info(f'warn_user from group {self.username}')
#         userid = self.userid

#         answer = f"""
# ⚠️Warning your subscription is ending soon please Renew it to have access VIP

# {wordpress_url}

# Info @{environment}

# {environment} forex Team
#         """
#         bot.send_message(userid, text=answer)

    def set_user_bst(self):
        # adds user to group and schedules date to kick user out
        logging.info(f'set_user_bst from group {self.username}')

        subscription = self.subscription
        userid = self.userid
        username = self.username
        channel_name = int(os.getenv("channel_name"))
        warn_date = self.subscription - datetime.timedelta(days=1)
        # warn_date = datetime.datetime.now() 
        value = asyncio.run(sleep_async(2))
        value = asyncio.run(main(self, channel_name))


        print('printing ', value)

        # try:
        #     unban_job = q.enqueue(unbanTask, userid, channel_name,  description=f"ppallow {self.username}")
        #     job = q.enqueue_in(datetime.timedelta(seconds=10), warnbanTask, userid, channel_name, description=f"warn usering {self.username}")
        #     warn_job = q.enqueue_at(warn_date, warnbanTask, userid, channel_name, description=f"warn user {self.username}")

        #     kick_job = q.enqueue_at(subscription, kickTask, userid, channel_name, description=f"kick_user {self.username}")
        # except:
        #     print("gjhkj")
        # jobwarn = scheduler.add_job(self.warn_user, 'date', run_date=warn_date,
        #                             id=str(userid) + ' warn', replace_existing=True, name=f"warn_user {self.username}")
        # job = scheduler.add_job(self.kick_user, 'date', run_date=subscription,
        #                         id=str(userid), replace_existing=True, name=f"kick_user {self.username}")
        # datetime.date.fromtimestamp(1694016856.557)
        # job.trigger.run_date
        answer = "all set"
        bot.send_message(userid, text=answer)
        return job

    def __repr__(self):
        return f'User {self.username}'


# class BstPage(Document):
#     title = StringField(max_length=200, required=True)
#     date_modified = DateTimeField(default=datetime.datetime.utcnow)
#     order_id = IntField(unique=True)
#     phone = IntField(unique=True)
#     product_id = IntField()
#     expire = DateTimeField()

# import pymongo
# client = pymongo.MongoClient("mongodb+srv://monitor:monitor>@realmcluster.yjlnu.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test
