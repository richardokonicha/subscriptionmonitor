# -*- coding: utf-8 -*-

from flask import Flask, request
# from urllib import unquote_plus
import json
import re
from api_methods import wcapi
import os

app = Flask(__name__)

def parse_request(req):
    """
    Parses application/json request body data into a Python dictionary
    """
    payload = req.get_data()
    # payload = unquote_plus(payload)
    payload = re.sub('payload=', '', payload)
    payload = json.loads(payload)

    return payload

@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 to see a message
    """
    return ('This is a website.', 200, None)

@app.route('/monitor/order', methods=['POST'])
def new_order_hook():
    """
    Send a POST request to localhost:5000/api/print with a JSON body with a "p" key
    to print that message in the server console.
    """
    request_object = request.stream.read().decode("utf-8")
    import pprint
    pprint.pprint(request_object)
    

    return (request_object, 200, None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


