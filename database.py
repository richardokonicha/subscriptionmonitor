from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('db_host')

connect('monitor_db', host=db_host)

from mongoengine import *
import datetime

class User(Document):
    # user object
    userid = IntField(unique=True)
    username = StringField()
    subscriptionstatus = StringField() # subscribed or unsubscribed
    orders = ListField(IntField())
    subscription = DateTimeField()
    
    def subscribed_to(self, productid, orderid):
        self.orders.append(orderid)

        if productid == 978:
            # 1 month subscription
            subscribed_time = datetime.timedelta(days=30)
        if productid == 1000:
            # 2 months subscription
            subscribed_time = datetime.timedelta(days=30)
        if productid == 2000:
            # 1 year subscription 
            subscribed_time = datetime.timedelta(days=365)
        
        self.subscription = self.subscription + subscribed_time


    def __repr__(self):
        return f'User {self.username}'


class BstPage(Document):
    title = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    order_id = IntField( unique=True)
    phone = IntField(unique=True)
    product_id = IntField()
    expire = DateTimeField()

# import pymongo
# client = pymongo.MongoClient("mongodb+srv://monitor:monitor>@realmcluster.yjlnu.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test
