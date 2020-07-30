"""
This example demonstrates the use of the MongoDB job store.
On each run, it adds a new alarm that fires after ten seconds.
You can exit the program, restart it and observe that any previous alarms that have not fired yet
are still active. Running the example with the --clear switch will remove any existing alarms.
"""


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import utc

from datetime import datetime, timedelta
import sys
import os

from apscheduler.schedulers.blocking import BlockingScheduler


import pymongo
client = pymongo.MongoClient(
    "mongodb+srv://monitor:monitor@realmcluster.yjlnu.mongodb.net/test?retryWrites=true&w=majority"
    )
db = client.test

def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


jobstores = {
    'mongo': MongoDBJobStore(client=client),
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
    # timezone=utc
    )
        # scheduler.add_jobstore(client=client, database=db, collection='example_jobs')

alarm_time = datetime.now() + timedelta(seconds=10)

scheduler.add_job(alarm, 'date', run_date=alarm_time, args=[datetime.now()])

print("hello world")

scheduler.start()



