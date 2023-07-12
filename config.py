from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import utc
from pymongo import MongoClient
from telebot import types, TeleBot
from woocommerce import API
from dotenv import load_dotenv
import os
from telethon.sessions import StringSession
from telethon import TelegramClient
import logging

logging.basicConfig()
logging.getLogger("apscheduler").setLevel(logging.DEBUG)
# logging.getLogger("telebot").setLevel(logging.DEBUG)
# import logging

# logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


load_dotenv()

#  select 2 premium group enviroment variable set 1 for bst environment
pipeline = 1
if pipeline == 1:
    load_dotenv(dotenv_path="bst.env")
if pipeline == 2:
    load_dotenv(dotenv_path="premium.env")

api_hash = os.getenv("api_hash")
api_id = os.getenv("api_id")
channel_link = os.getenv("channel_link")
ckey = os.getenv("ckey")
csecret = os.getenv("csecret")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
debug = os.getenv("debug") == "True"
environment = os.getenv("environment")
fugoku_url = os.getenv("fugoku_url")
sentrydsn = os.getenv("sentrydsn")
sessionString = os.getenv("sessionString")
token = os.getenv("token")
wordpress_url = os.getenv("wordpress_url")
channel_name = int(os.getenv("channel_name"))
admin_id = os.getenv("admin_id")

MONTHLY=int(os.getenv("MONTHLY"))
BIMONTHLY=int(os.getenv("BIMONTHLY"))
YEARLY=int(os.getenv("YEARLY"))
LIFETIME=int(os.getenv("LIFETIME"))



print(f"Environment is {environment}")

join_channel_markup = types.InlineKeyboardMarkup()
join_channel_button = types.InlineKeyboardButton(
    text="Join Now ✅", url=channel_link, callback_data="join_channel"
)
join_channel_markup.add(join_channel_button)

wcapi = API(
    timeout=10,
    url=wordpress_url,
    consumer_key=ckey,
    consumer_secret=csecret,
    wp_api=True,
    version="wc/v3",
    query_string_auth=True,
)

bot = TeleBot(token, threaded=True)

# bot_client = TelegramClient(StringSession(sessionString), api_id, api_hash)

client = MongoClient(db_host)

jobstores = {
    "mongo": MongoDBJobStore(client=client, database=db_name),
    # "default": MongoDBJobStore(client=client, database=db_name),
}
executors = {
    # 'default': ThreadPoolExecutor(20),
    # 'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    # 'coalesce': False,
    "max_instances": 3,
    "misfire_grace_time": 259200,
}
scheduler = BackgroundScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc
)
