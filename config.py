from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
import pymongo
import telebot
from woocommerce import API
from dotenv import load_dotenv
import os
load_dotenv()

ckey = os.getenv("ckey")
csecret = os.getenv("csecret")
debug = (os.getenv("DEBUG") == 'True')
token = os.getenv("token")
url = os.getenv("url")
bst_url = os.getenv("bst_url")


wcapi = API(
    url=bst_url,
    consumer_key=ckey,
    consumer_secret=csecret,
    version="wc/v3"
)

bot = telebot.TeleBot(
    token,
    threaded=True
)

# scheduler


client = pymongo.MongoClient(
    "mongodb+srv://monitor:monitor@realmcluster.yjlnu.mongodb.net/test?retryWrites=true&w=majority"
)

jobstores = {
    'default': MongoDBJobStore(client=client, database="test", HOST="realmcluster-shard-00-02.yjlnu.mongodb.net"),
    # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc
)

# r = wcapi.get("orders?completed")

# print(wcapi.get("orders/727").json())

# import pprint
# pprint.pprint(r.json())
# print(r.status_code)
