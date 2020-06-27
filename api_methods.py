from woocommerce import API
from dotenv import load_dotenv
load_dotenv()
import os

ckey = os.getenv("ckey")
csecret = os.getenv("csecret")
url = "www.bst-forexgroup.com"

wcapi = API(
    url=url,
    consumer_key=ckey,
    consumer_secret=csecret,
    version="wc/v3"
)
