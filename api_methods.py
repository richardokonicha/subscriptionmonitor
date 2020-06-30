from woocommerce import API
from dotenv import load_dotenv
load_dotenv()
import os

ckey = os.getenv("ckey")
csecret = os.getenv("csecret")
url = "http://www.bst-forexgroup.com/"

wcapi = API(
    url=url,
    consumer_key=ckey,
    consumer_secret=csecret,
    version="wc/v3"
)

r = wcapi.get("orders?completed")



import pprint
pprint.pprint(r.json())
print(r.status_code)