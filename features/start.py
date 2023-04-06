import re
import telebot
import database as db
import datetime
import asyncio
import requests
import time
import os
import logging

from telebot import types
from unsync import unsync
from telethon.sync import TelegramClient
from config import (
    api_id,
    api_hash,
    sessionString,
    environment,
    wordpress_url,
    bot,
    wcapi,
    scheduler,
    channel_link,
    channel_name,
)
from telethon.sessions import StringSession
from messages import description

from telethon.tl.functions.messages import (
    AddChatUserRequest,
    GetFullChatRequest,
    SendMessageRequest,
)
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from telethon.tl.functions.messages import SendReactionRequest

from helpers import (get_product_order, get_woo_data, get_order, warn_user, kick_user, revoke_access, grant_access, check_group, schedule_renew)

def start(message):
    try:
        userid = message.from_user.id
        chat_id = message.chat.id
        message_id = message.message_id
        if not message.from_user.username:
            return bot.send_photo(
                userid,
                photo="https://i1.wp.com/www.swipetips.com/wp-content/uploads/2021/03/tap-your-current-telegram-username.png?resize=300%2C285&ssl=1",
                caption="Your Telegram account doesn't have a username, set a username and try again."
            )
            
        bot.send_chat_action(userid, action="typing")

        bst_user = db.User.objects(userid=userid).first()
        if bst_user is None:
            username = message.from_user.username
            # create new user
            bst_user = db.User(userid=userid, username=username)
            bst_user.save()
        else:
            username = message.from_user.username
            bst_user.username = username
            bst_user.save()

        text = message.text
        load_match = re.match("(/start )([0-9]+)", text)
        if load_match is None:
            return bot.send_message(userid, text="No order placed")

        orderid = int(load_match.groups()[1])
        # checks if orderid has been used
        checkorder = db.User.objects(orders=orderid)
        if not checkorder:
            data = get_order(orderid)
            if data["productid"] is None:
                return bot.send_message(userid, text=data["msg"])
            if data["productid"]:
                bot.send_message(userid, text=f"{data['msg']}")
            bot.send_chat_action(userid, action="typing")
            bot.send_message(userid, text="Processing ...")

            productid = data["productid"]
            ordername = data["ordername"]
            subscribedto = bst_user.subscribed_to(productid, orderid)
            translated_subscribedto = subscribedto.strftime("%A %d %B %Y")

            access_sync = grant_access(bst_user)
            access_result = access_sync.result()
            renew = schedule_renew(bst_user)

            if orderid != 101010:
                bst_user.orders.append(orderid)
                bst_user.save()

            ordername = re.sub(r'\W+', " ", ordername)
            answer = description["subscription_started"].format(
                username=username.replace("_", "\_"),
                ordername=ordername,
                subscribedto=translated_subscribedto,
                environment=environment,
                channel_link=channel_link,
            )
            join_channel_markup = telebot.types.InlineKeyboardMarkup()
            join_channel_button = telebot.types.InlineKeyboardButton(
                text="Join Now ✅", url=channel_link, callback_data="join_channel"
            )
            join_channel_markup.add(join_channel_button)
        else:
            answer = f"Order number {orderid} has already been used"
            join_channel_markup = None

        bot.send_message(
            userid,
            text=answer,
            parse_mode="MarkdownV2",
            reply_markup=join_channel_markup,
        )

    except Exception as e:
        print("an error has occurred", e)
        logging.error(e)


@bot.callback_query_handler(func=lambda call: call.data == "join_channel")
def join_channel(call):
    user_id = call.from_user.id
    message_id = call.message.message_id
    pass
