from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('db_host')

connect('monitor_db', host=db_host)

from mongoengine import *
import datetime

class Page(Document):
    title = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

# import pymongo
# client = pymongo.MongoClient("mongodb+srv://monitor:monitor>@realmcluster.yjlnu.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test
