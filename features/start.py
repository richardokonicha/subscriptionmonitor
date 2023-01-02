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
    bot_client,
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


def get_product_order(woo_data, orderid):
    logging.warning(f"Getting product order info {orderid}")
    msg = ""
    productid = None
    ordername = None
    if orderid == 101010:
        productid = 101010
        ordername = "3 minutes test"
        msg = "This is a test 101010"
    else:
        try:
            productid = woo_data["line_items"][0]["product_id"]
            ordername = woo_data["line_items"][0]["name"]
            msg = f"{ordername} Order placed"
        except KeyError as e:
            msg = "Invalid Order ID please place an order"
    order = {"productid": productid, "ordername": ordername, "msg": msg}
    logging.warning(f"Product order info retrived {ordername, msg}")
    return order


def get_woo_data(load):
    logging.warning("Getting order from woocommerce")
    data = {}
    try:
        data = wcapi.get(f"orders/{load}").json()
    except requests.exceptions.ReadTimeout:
        print("Timeout occurred, trying again")
        time.sleep(3)
        get_order(load)
    logging.warning(f"Woocommerce returned \n")
    return data


def get_order(orderid):
    logging.warning(f"Getting order info {orderid}")
    woo_data = get_woo_data(orderid)
    order = get_product_order(woo_data, orderid)

    logging.warning(f"Order data retrived <{order['msg']}> \n")

    return order


def warn_user(bst_user):
    # warns user from group
    logging.info(f"warn_user from group {bst_user.username}")
    userid = bst_user.userid
    username = bst_user.username
    answer = description["warn_subscription"].format(
        wordpress_url=wordpress_url,
        environment=environment,
        username=username,
        channel_link=channel_link,
    )
    bot.send_message(userid, text=answer, parse_mode="MarkdownV2")


def kick_user(bst_user):
    logging.info(f"kicks user from group {bst_user.username}")

    userid = bst_user.userid
    username = bst_user.username

    kick_sync = revoke_access(userid, channel_name, username)
    kick_result = kick_sync.result

    answer = description["subscription_ended"].format(
        wordpress_url=wordpress_url,
        environment=environment,
        username=username,
        channel_link=channel_link,
    )

    bot.send_message(userid, text=answer, parse_mode="MarkdownV2")
    print("kicked user lol")
    return


@unsync
async def revoke_access(userid, channel_name, username):

    logging.info(f"async kick user from channel {userid}")
    try:
        await bot_client.connect()
        channel = await bot_client.get_entity(channel_name)
        user = await bot_client.get_entity(userid)
    except:
        user = await bot_client.get_entity(username)
    await asyncio.sleep(1)

    try:
        msg = description["revoke_access"].format(
            wordpress_url=wordpress_url,
            environment=environment,
            username=username,
            channel_link=channel_link,
        )
        # result = await bot_client.edit_permissions(channel, user, view_messages=True)
        result = await bot_client(
            EditBannedRequest(
                channel.id, user, ChatBannedRights(until_date=None, view_messages=True)
            )
        )
        bot.send_message(
            userid,
            text=msg,
            parse_mode="MarkdownV2",
        )

    except Exception as e:
        print(e)
        logging.error(msg, e)

    await bot_client.disconnect()
    return user


@unsync
async def grant_access(user):
    userid = user.userid
    username = user.username

    logging.info(f"async add users to channel {username}")
    try:
        await bot_client.connect()

        channel_name = int(os.getenv("channel_name"))
        channel = await bot_client.get_entity(channel_name)

        print("fetching user by id")
        user = await bot_client.get_entity(userid)
    except Exception as e:
        print("fetching user by username", e)
        user = await bot_client.get_entity(username)
    else:
        print("Everything is ok.")
    try:
        check = await check_group(userid, channel)

        if check:
            msg = f"🟢 Subscription Renewed"
            try:
                # result = await bot_client.edit_permissions(channel, user,until_date=None, view_messages=False)
                result = await bot_client(
                    EditBannedRequest(
                        channel.id,
                        user,
                        ChatBannedRights(until_date=None, view_messages=False),
                    )
                )
                bot_client.disconnect()
                bot.send_message(
                    userid,
                    text=msg,
                    parse_mode="MarkdownV2",
                )
            except Exception as e:
                print(e)
        else:
            msg = f"🟢 Congratulations {channel.title}"
            try:
                # result = await bot_client.edit_permissions(channel, user,until_date=None, view_messages=False)
                # bot.send_message(userid, text=msg)
                result = await bot_client(
                    EditBannedRequest(
                        channel.id,
                        user,
                        ChatBannedRights(until_date=None, view_messages=False),
                    )
                )
                bot.send_message(
                    userid,
                    text=msg,
                    parse_mode="MarkdownV2",
                )
            except Exception as e:
                print(e)

        await asyncio.sleep(1)

        value = {
            "channel": channel.title,
            "msg": msg,
            "user": {"userid": userid, "username": username},
        }
        return value

    except Exception as e:
        print("An error occurred!", e)
        return


async def check_group(user_to_add, channel):
    await bot_client.start()
    logging.info(f"Checking group {user_to_add}")
    async for user in bot_client.iter_participants(channel):
        if user_to_add == user.id:
            return True
    return False


def schedule_renew(bst_user):
    warn_date = bst_user.subscription - datetime.timedelta(days=1)

    translated_warndate = warn_date.strftime("%A %d %B %Y")

    logging.info(f"warning on {translated_warndate}")
    print(f"warning on {translated_warndate}")

    jobwarn = scheduler.add_job(
        warn_user,
        "date",
        args=[bst_user],
        run_date=warn_date,
        id=str(bst_user.userid) + " warn",
        replace_existing=True,
        name=f"warn_user {bst_user.username}",
    )
    job = scheduler.add_job(
        kick_user,
        "date",
        args=[bst_user],
        run_date=bst_user.subscription,
        id=str(bst_user.userid),
        replace_existing=True,
        name=f"kick_user {bst_user.username}",
    )
    return True


def start(message):
    try:
        userid = message.from_user.id

        chat_id = message.chat.id
        message_id = message.message_id
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
            access_result = access_sync.result
            renew = schedule_renew(bst_user)

            if orderid != 101010:
                bst_user.orders.append(orderid)
                bst_user.save()

            answer = description["subscription_started"].format(
                username=username,
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
