import datetime
from mongoengine import *
from mongoengine import connect
from dotenv import load_dotenv
import os
from telethon_client import bot_client, main, kick
from config import scheduler, bot

load_dotenv()

db_host = os.getenv('db_host')

connect('monitor_db', host=db_host)


class User(Document):
    # user object
    userid = IntField(unique=True)
    username = StringField()
    subscriptionstatus = StringField()  # subscribed or unsubscribed
    orders = ListField(IntField())
    subscription = DateTimeField(default=datetime.datetime.now())

    def checksub(self):
        if bool(self.subscription) == False:
            return False
        else:
            if self.subscription <= datetime.datetime.now():
                return False
            else:
                return self.subscription - datetime.datetime.now()

    def addsubscription(self, subscribed_time):
        sub = self.checksub()
        if sub == False:
            self.subscription = datetime.datetime.now() + subscribed_time
            self.save()
            return self.subscription
        else:
            self.subscription = self.subscription + subscribed_time
            self.save()
            return self.subscription

    def subscribed_to(self, productid, orderid):
        # self.orders.append(orderid)
        if productid == 101010:
            subscribed_time = datetime.timedelta(minutes=3)

        if productid == 978:
            # 1 month subscription
            subscribed_time = datetime.timedelta(days=30)

        if productid == 979:
            # 2 months subscription
            subscribed_time = datetime.timedelta(days=60)

        if productid == 980:
            # 1 year subscription
            subscribed_time = datetime.timedelta(days=365)

        if productid == 981:
            # 1 year subscription
            subscribed_time = datetime.timedelta(days=1820)

        subscription = self.addsubscription(subscribed_time)
        job = self.set_user_bst()
        return subscription

    def warn_user(self):
        # warns users and sets date to be kicked out
        userid = self.userid
        subscription = self.subscription
        job = scheduler.add_job(self.kick_user, 'date', run_date=subscription,
                                id=str(userid), replace_existing=True)
        answer = "Warning your subscription would expire soon please renew"
        bot.send_message(userid, text=answer)

    def kick_user(self):
        # kicks user from group
        userid = self.userid
        channel_name = os.getenv("channel_name")
        main_value = bot_client.loop.run_until_complete(
            kick(userid, channel_name))

        answer = main_value['newuser']
        bot.send_message(userid, text=answer)

        print("kicked user lol")

    def set_user_bst(self):
        # adds user to group and schedules date to kick user out
        subscription = self.subscription
        userid = self.userid
        channel_name = os.getenv("channel_name")

        bot_client.start()
        main_value = bot_client.loop.run_until_complete(
            main(userid, channel_name))

        warn_date = subscription - datetime.timedelta(days=1)

        job = scheduler.add_job(self.warn_user, 'date', run_date=warn_date,
                                id=str(userid), replace_existing=True)
        # datetime.date.fromtimestamp(1694016856.557)
        # job.trigger.run_date
        answer = main_value['newuser']
        bot.send_message(userid, text=answer)

        return job

    def __repr__(self):
        return f'User {self.username}'


class BstPage(Document):
    title = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    order_id = IntField(unique=True)
    phone = IntField(unique=True)
    product_id = IntField()
    expire = DateTimeField()

# import pymongo
# client = pymongo.MongoClient("mongodb+srv://monitor:monitor>@realmcluster.yjlnu.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test
