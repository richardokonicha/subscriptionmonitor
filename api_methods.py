from woocommerce import API
from dotenv import load_dotenv
load_dotenv()
import os

# ckey = os.getenv("ckey")
# csecret = os.getenv("csecret")
url = "https://www.bst-forexgroup.com/"

ckey = "ck_b84a2b10b2ddd451f10306100e54f7c505e3cb76"
csecret = "cs_acb181069525e833b00b90c0b8e6139da37f0b87"

wcapi = API(
    url=url,
    consumer_key=ckey,
    consumer_secret=csecret,
    version="wc/v3"
)

r = wcapi.get("products")
print(r.status_code)