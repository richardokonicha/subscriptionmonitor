import pymongo
from apscheduler.schedulers.blocking import BlockingScheduler
# import datetime
import sys
from datetime import datetime, timedelta
from pytz import utc
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from telethon import TelegramClient
from dotenv import load_dotenv
import os
import time
load_dotenv
# Remember to use your own values from my.telegram.org!

# api_id = os.getenv("api_id")
# api_hash = os.getenv("api_hash")
# client = TelegramClient('anon', api_id, api_hash)
# client = TelegramClient('anon', 1347918, '5681581438678d9390cd4f67ee764f82')

# async def main():
#     # Getting information about yourself
#     me = await client.get_me()
#     print(me.stringify())
#     async for dialog in client.iter_dialogs():
#         print(dialog.name, 'has ID', dialog.id)

#     # You can send messages to yourself...
#     await client.send_message('me', 'Hello, myself!')

# client = TelegramClient('anon', 1347918, '5681581438678d9390cd4f67ee764f82')
# client.start()
# client.kick_participant
# client.disconnect()


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
scheduler = BlockingScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc
)


def plam():
    print('Alarm! This alarm was scheduled ')


def flam():
    print('Flam This alarm was scheduled ')


ptime = datetime.utcnow() + timedelta(seconds=60)
ltime = datetime.utcnow() + timedelta(seconds=5)

# scheduler.add_job(plam, 'date', run_date=ptime)
scheduler.add_job(flam, 'date', run_date=ltime, id="lptime_id")

# print("hello world")
# utime = datetime.now() + timedelta(seconds=15)
# scheduler.reschedule_job('lptime_id', trigger='cron', minute='*/1')

scheduler.start()
