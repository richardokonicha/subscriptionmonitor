# -*- coding: utf-8 -*-

import importdir
from flask import Flask, request
# from urllib import unquote_plus
import json
import re
from config import (scheduler, wcapi, token, debug, fugoku_url, bot, telebot)
import os
import sentry_sdk
importdir.do("features", globals())

server = Flask(__name__)

sentry_sdk.init(
    dsn="https://3f05ccb579b446be8ecbc24fe17c4478@o4504356168597504.ingest.sentry.io/4504356174757888",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    traces_sampler=1
    
)
scheduler.start()

@server.route('/', methods=['GET'])
def index():
    return ('This is a website.', 200, None)


@server.route('/monitor/order', methods=['POST'])
def new_order_hook():
    request_object = request.stream.read().decode("utf-8")
    return (request_object, 200, None)


@server.route('/' + token, methods=['POST'])
def getMessage():
    request_object = request.stream.read().decode("utf-8")
    update_to_json = [telebot.types.Update.de_json(request_object)]
    bot.process_new_updates(update_to_json)
    return "got Message bro"


@server.route('/hook')
def webhook():
    jurl = fugoku_url
    bot.remove_webhook()
    bot.set_webhook(jurl + token)
    return f"Webhook set to {fugoku_url}"


if debug == True:
    bot.remove_webhook()
    bot.polling()
else:
    if __name__ == "__main__":
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5001)))
