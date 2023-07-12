import datetime
import requests
import time
import os
import logging

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
    admin_id
)
from telethon.sessions import StringSession
from messages import description

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights


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
            sendError(e)
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
        username=username.replace("_", "\_"),
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
        username=username.replace("_", "\_"),
        channel_link=channel_link,
    )

    bot.send_message(userid, text=answer, parse_mode="MarkdownV2",
                     disable_web_page_preview=True)
    print("kicked user lol")
    return


@unsync
async def revoke_access(userid, channel_name, username):
    bot_client = TelegramClient(StringSession(sessionString), api_id, api_hash)
    logging.info(f"async kick user from channel {userid}")

    try:
        try:
            await bot_client.connect()
            channel = await bot_client.get_entity(channel_name)
            user = await bot_client.get_entity(username)
        except:
            user = await bot_client.get_entity(userid)

        msg = description["revoke_access"].format(
            wordpress_url=wordpress_url,
            environment=environment,
            username=username.replace("_", "\_"),
            channel_link=channel_link,
        )

        # result = await bot_client.edit_permissions(channel, user, view_messages=True)
        result = await bot_client(
            EditBannedRequest(
                channel, user, ChatBannedRights(
                    until_date=None, view_messages=True)
            )
        )
        bot.send_message(
            userid,
            text=msg,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True
        )

    except Exception as e:
        print(e)
        logging.error(msg, e)
        sendError(e)

    await bot_client.disconnect()
    return user


@unsync
async def grant_access(user):
    userid = user.userid
    username = user.username
    try:
        bot_client = TelegramClient(
            StringSession(sessionString), api_id, api_hash)
        await bot_client.connect()

        logging.info(f"async add users to channel {username}")
        try:
            channel_name = int(os.getenv("channel_name"))
            channel = await bot_client.get_entity(channel_name)

            print("fetching user by username")
            user = await bot_client.get_entity(username)
        except Exception as e:
            print("fetching user by id")
            user = await bot_client.get_entity(userid)
        else:
            print("Everything is ok.")

        check = await check_group(userid, channel, bot_client)

        if check:
            msg = f"🟢 Subscription Renewed"
            try:
                # result = await bot_client.edit_permissions(channel, user,until_date=None, view_messages=False)
                result = await bot_client(
                    EditBannedRequest(
                        channel,
                        user,
                        ChatBannedRights(until_date=None, view_messages=False),
                    )
                )
                print("Grant access")
                bot.send_message(
                    userid,
                    text=msg,
                    parse_mode="MarkdownV2",

                )
            except Exception as e:
                print(e)
                sendError(e)
        else:
            msg = f"🟢 Congratulations {channel.title}"
            try:
                # result = await bot_client.edit_permissions(channel, user,until_date=None, view_messages=False)
                result = await bot_client(
                    EditBannedRequest(
                        channel,
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
                sendError(e)
                return e

    except Exception as e:
        print("An error occurred!", e)
        sendError(e)
        return e

    await bot_client.disconnect()
    value = {
        "channel": channel.title,
        "msg": msg,
        "user": {"userid": userid, "username": username},
    }
    return value


async def check_group(user_to_add, channel, bot_client):
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
        jobstore='mongo'
    )
    job = scheduler.add_job(
        kick_user,
        "date",
        args=[bst_user],
        run_date=bst_user.subscription,
        id=str(bst_user.userid),
        replace_existing=True,
        name=f"kick_user {bst_user.username}",
        jobstore='mongo'
    )
    return True


def sendError(error):
    error_text = f'{str(error)} {error.message}'
    print("Reporting erorr", error_text)
    return bot.send_message(admin_id, text=error_text)
