import datetime
from mongoengine import *
from mongoengine import connect
from dotenv import load_dotenv
import os
from telethon_client import bot as client_bot, main, kick
from config import scheduler

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
        if productid == 978:
            # 1 month subscription
            subscribed_time = datetime.timedelta(days=30)

        if productid == 979:
            # 2 months subscription
            subscribed_time = datetime.timedelta(days=60)

        if productid == 2000:
            # 1 year subscription
            subscribed_time = datetime.timedelta(days=365)

        subscription = self.addsubscription(subscribed_time)
        job = self.set_user_bst()
        return subscription

    def kick_user(self):
        # kicks user from group
        userid = self.userid
        client_bot.loop.run_until_complete(kick(userid))
        print("kicked user lol")

    def set_user_bst(self):
        # adds user to group and schedules date to kick user out
        subscription = self.subscription
        userid = self.userid

        client_bot.start()
        client_bot.loop.run_until_complete(main(userid))
        job = scheduler.add_job(self.kick_user, 'date', run_date=subscription,
                                id=str(userid), replace_existing=True)
        # datetime.date.fromtimestamp(1694016856.557)
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
