from flask import Flask, request, render_template
import json
import re
from unsync import unsync
import uvicorn

from config import (
    scheduler,
    wcapi,
    token,
    debug,
    fugoku_url,
    bot,
    types,
    sentrydsn,
    channel_name,
    bot_client,
)
import os
import sentry_sdk
from features.start import start
from features.status import status
from features.dashboard import dashboard

from telethon.tl.functions.photos import GetUserPhotosRequest

server = Flask(__name__)

sentry_sdk.init(
    dsn=sentrydsn,
    traces_sample_rate=1.0,
    traces_sampler=1,
)
scheduler.start()


@bot.message_handler(commands=["dashboard", "Dashboard"])
def dashboard_command(message):
    try:
        dashboard(message)
    except Exception as e:
        print("Error occurred on dashboard", e)


@bot.message_handler(commands=["start", "Start"])
def start_command(message):
    try:
        start(message)
    except Exception as e:
        print("Error occurred on start", e)


@bot.message_handler(commands=["status", "Status"])
def status_commandd(message):
    try:
        status(message)
    except Exception as e:
        print("Error occurred on status", e)


@server.route("/", methods=["GET"])
def index():
    return ("This is a website.", 200, None)


@server.route("/monitor/order", methods=["POST"])
def new_order_hook():
    request_object = request.stream.read().decode("utf-8")
    return (request_object, 200, None)


@server.route("/" + token, methods=["POST"])
def getMessage():
    request_object = request.stream.read().decode("utf-8")
    update_to_json = [types.Update.de_json(request_object)]
    bot.process_new_updates(update_to_json)
    return "got Message bro"


@server.route("/hook")
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
        server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
