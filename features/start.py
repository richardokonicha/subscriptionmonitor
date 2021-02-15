from config import bot, wcapi, scheduler, channel_link, environment
import re
import telebot
from database import BstPage
import database as db
# from telethon_client import bot_client, main, kick
# from utils import cll
import asyncio
import requests
import time


def get_order(load):
    data = {}
    try:
        data = wcapi.get(f"orders/{load}").json()
    except requests.exceptions.ReadTimeout:
        
        print("Timeout occurred, trying again")
        time.sleep(3)
        # data = wcapi.get(f"orders/{load}").json()
        get_order(load)
    return data


@bot.message_handler(commands=["start", "Start"])
def start(message):
    userid = message.from_user.id
    # get user object
    bot.send_chat_action(userid, action='typing')
    bst_user = db.User.objects(userid=userid).first()
    if bst_user == None:
        username = message.from_user.username
        # create new user
        bst_user = db.User(
            userid=userid,
            username=username
        )
        bst_user.save()
    else:
        username = bst_user.username = message.from_user.username
        bst_user.save()

    text = message.text

    load = re.match("(/start )([0-9]+)", text)
    if not bool(load):
        answer = "No order placed"
        return bot.send_message(userid, text=answer)

    load = load.groups()[1]
    orderid = int(load)
    # checks if orderid has been used
    checkorder = db.User.objects(orders=orderid)
    if bool(checkorder) == False:
        data = get_order(orderid)
        # adds orderid to list of orders
        if orderid == 101010:
            # for test
            productid = 101010
            ordername = "3 minutes test"
        else:
            # bst_user.orders.append(orderid)
            # bst_user.save()
            try:
                productid = data['line_items'][0]['product_id']
                ordername = data['line_items'][0]['name']
            except KeyError:
                answer = "Invalid Order ID please place an order"
                return bot.send_message(userid, text=answer)
        bot.send_chat_action(userid, action='typing')
        bot.send_message(userid, text='Processing ...')

        # adds product subscribtion days and stores the order number
        subscribedto = bst_user.subscribed_to(
            productid, orderid).strftime("%A %d %B %Y")

        if orderid != 101010:
            bst_user.orders.append(orderid)
            bst_user.save()
        answer = f"""
Hi {username},

🟢Your subscription for {ordername} has been processed 

You now have access to Premium VIP forex signals

Your subscription would last until {subscribedto}

PLEASE READ THE PINNED MESSAGE IN VIP AND FOLLOW MONEY MANAGEMENT! 

Info @{environment}trading

{environment} forex Team

Click this link to join
    """
        join_channel_markup = telebot.types.InlineKeyboardMarkup()
        join_channel_button = telebot.types.InlineKeyboardButton(
            text="Join Now ✅", url=channel_link, callback_data="join_channel")
        join_channel_markup.add(join_channel_button)
    else:
        answer = f"""Order number {orderid} has already been used"""
        join_channel_markup = None

    bot.send_message(userid, text=answer, reply_markup=join_channel_markup)


@bot.callback_query_handler(func=lambda call: call.data == "join_channel")
def join_channel(call):
    user_id = call.from_user.id
    message_id = call.message.message_id
    pass
