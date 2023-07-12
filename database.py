import datetime
import logging

# from mongoengine import *
from mongoengine import (
    connect,
    DateTimeField,
    ListField,
    StringField,
    IntField,
    Document,
)
from config import db_host, db_name, MONTHLY, YEARLY, BIMONTHLY, LIFETIME


connect(db_name, host=db_host)


class User(Document):
    userid = IntField(unique=True)
    username = StringField()
    subscriptionstatus = StringField()
    orders = ListField(IntField())
    subscription = DateTimeField(default=datetime.datetime.utcnow())

    def checksub(self):
        logging.info("Checking sub")

        if bool(self.subscription) == False:
            return False
        else:
            if self.subscription <= datetime.datetime.utcnow():
                return False
            else:
                return self.subscription - datetime.datetime.utcnow()

    def addsubscription(self, subscribed_time):
        logging.info("addsubscription ")

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
            subscribed_time = datetime.timedelta(minutes=0.5)

        if productid == MONTHLY:
            # 1 month subscription
            subscribed_time = datetime.timedelta(days=30)

        if productid == BIMONTHLY:
            # 2 months subscription
            subscribed_time = datetime.timedelta(days=60)

        if productid == YEARLY:
            # 1 year subscription
            subscribed_time = datetime.timedelta(days=365)

        if productid == LIFETIME:
            # Lifetime subscription
            subscribed_time = datetime.timedelta(weeks=4000)

        try:
            if subscribed_time:
                subscription = self.addsubscription(subscribed_time)
            else:
                print("subscribed time is null")
            return subscription
        except Exception as e:
            print("Problem with product id please check", productid)
            logging.info("Problem with product id please check ")
            return None

    def __repr__(self):
        return f"User {self.username}"
