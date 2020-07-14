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

wcapi = API(
    url=url,
    consumer_key=ckey,
    consumer_secret=csecret,
    version="wc/v3"
)

bot = telebot.TeleBot(
    token, 
    threaded=True
    )

# r = wcapi.get("orders?completed")

# print(wcapi.get("orders/727").json())

# import pprint
# pprint.pprint(r.json())
# print(r.status_code)