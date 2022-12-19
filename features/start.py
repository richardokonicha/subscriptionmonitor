from config import bot, wcapi, scheduler, channel_link, environment, bot_client
import re
import telebot
import database as db
import datetime
import asyncio
import requests
import time
import os
import logging
from telethon.sync import TelegramClient
from config import api_id, api_hash, sessionString, environment, wordpress_url
from telethon.sessions import StringSession
from interface import add_to_queue, get_job_status
# from bst_entity import add_user as add_t
from messages import description

from telethon_client import main, kick, unbanTask, warnbanTask, kickTask
from config import scheduler, bot, wordpress_url, environment, bot_client
import logging
from interface import add_to_queue, report_success, report_failure, q
import asyncio

from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights



def get_product_order(woo_data, orderid):
    logging.warning(f"Getting product order info {orderid}")
    msg = ''
    productid = None
    ordername = None
    if orderid == 101010:
        productid = 101010
        ordername = "3 minutes test"
        msg = 'This is a test 101010'
    else:
        try:
            productid = woo_data['line_items'][0]['product_id']
            ordername = woo_data['line_items'][0]['name']
            msg = f"{ordername} Order placed"
        except KeyError as e:
            msg = "Invalid Order ID please place an order"
    order = { 'productid': productid, 'ordername': ordername, 'msg': msg}
    logging.warning(f"Product order info retrived {ordername, msg}")
    return order

def get_woo_data(load):
    logging.warning('Getting order from woocommerce')
    data = {}
    try:
        data = wcapi.get(f"orders/{load}").json()
    except requests.exceptions.ReadTimeout:
        print("Timeout occurred, trying again")
        time.sleep(3)
        get_order(load)
    logging.warning(f"Woocommerce returned {data['message']} \n")
    return data

def get_order(orderid):
    logging.warning(f"Getting order info {orderid}")
    woo_data = get_woo_data(orderid)
    order = get_product_order(woo_data, orderid)

    logging.warning(f"Order data retrived <{order['msg']}> \n")

    return order

def warn_user(bst_user):
    # warns user from group
    logging.info(f'warn_user from group {bst_user.username}')
    userid = bst_user.userid

    answer = description['warn_subscription'].format(wordpress_url=wordpress_url, environment=environment)
    bot.send_message(userid, text=answer)

def kick_user(bst_user):
    # kicks user from group
    logging.info(f'kicks user from group {bst_user.username}')

    userid = bst_user.userid
    username = bst_user.username
    channel_name = int(os.getenv("channel_name"))

    # kick_job = q.enqueue_at(subscription, kickTask, userid, channel_name, description=f"kick_user {self.username}")


    access = asyncio.run(revoke_access(userid, channel_name, username))

    # bot_client.start()
    # main_value = bot_client.loop.run_until_complete(
    #     revoke_access(userid, channel_name, username))

    answer = description['subscription_ended'].format(wordpress_url=wordpress_url, environment=environment)

    bot.send_message(userid, text=answer)
    print("kicked user lol")
    return


async def revoke_access(userid, channel_name, username):

    bot_client = TelegramClient(StringSession(sessionString), api_id, api_hash)

    logging.info(f'async kick user from channel {userid}')
    try:
        await bot_client.connect()
        channel = await bot_client.get_entity(channel_name)
        user = await bot_client.get_entity(userid)
    except:
        user = await bot_client.get_entity(username)
    await asyncio.sleep(1)

    try:
        msg = description['revoke_access'].format(wordpress_url=wordpress_url, environment=environment)
        # result = await bot_client.edit_permissions(channel, user, view_messages=True)
        result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=True)))
        bot.send_message(userid, text=msg)

        # result2 = await bot_client.kick_participant(channel, user, ban=True)

    except Exception as e:
        print(e)
        logging.error(msg, e)

    # result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=True)))
    # subscription_ended = description['subscription_ended']
    # return {"channel": channel.title, "newuser": subscription_ended}
    await bot_client.disconnect()

    return user


async def grant_access(user):
    # checks if user is in a group and add users to channel/ group

    userid = user.userid
    username = user.username

    logging.info(f'async add users to channel {username}')
    try:
        await bot_client.connect()

        channel_name = int(os.getenv("channel_name"))
        channel = await bot_client.get_entity(channel_name)

        print('fetching user by id')
        user = await bot_client.get_entity(userid)
    except Exception as e:
        print('fetching user by username', e)
        user = await bot_client.get_entity(username)
    # except:
    #     print('couldnt get this user')
    else:
        print("Everything is ok.")
    try:
        check = await check_group(userid, channel)

        if check:
            msg = f'🟢 Subscription Renewed'
            try:
                # result = await bot_client.edit_permissions(channel, user,until_date=None, view_messages=False)
                result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
                bot_client.disconnect()
                bot.send_message(userid, text=msg)
            except Exception as e:
                print(e)
        else:
            msg = f'🟢 Congratulations! {channel.title}'
            try:

                # result = await bot_client.edit_permissions(channel, user,until_date=None, view_messages=False)
                # bot.send_message(userid, text=msg)
                result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
                bot.send_message(userid, text=msg)
                # result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
            except Exception as e:
                print(e)

        await asyncio.sleep(1)
        

        value = {"channel": channel.title, "msg": msg, "user": {'userid': userid, 'username': username}}
        return value

    except Exception as e:
        print("An error occurred!", e)
        return 

async def check_group(user_to_add, channel):
    await bot_client.start()
    logging.info(f'Checking group {user_to_add}')
    async for user in bot_client.iter_participants(channel):
        if user_to_add == user.id:
            return True
    return False

async def sleep_async(user, seconds):
    await asyncio.sleep(seconds)
    print("Woke up after {} seconds".format(seconds))
    
    userid = user.userid
    username = user.username

    logging.info(f'async add users to channel {username}')
    try:
        await bot_client.start()

        channel_name = int(os.getenv("channel_name"))
        channel = await bot_client.get_entity(channel_name)

        print('fetching user by id')
        user = await bot_client.get_entity(userid)
    except Exception as e:
        print('fetching user by username', e)
        user = await bot_client.get_entity(username)
    # except:
    #     print('couldnt get this user')
    else:
        print("Everything is ok.")


    try:
        check = await check_group(userid, channel)

        if check:
            msg = f'🟢 Subscription Renewed'
            # result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))
        else:
            msg = f'🟢 Congratulations! {channel.title}'
            # result = await bot_client(EditBannedRequest(channel.id, user, ChatBannedRights(until_date=None, view_messages=False)))

    except Exception as e:
        print("An error occurred!", e)
        return e

    value = {"channel": channel.title, "msg": msg, "user": {'userid': userid, 'username': username}}


    return value

def schedule_renew(bst_user):
    warn_date = bst_user.subscription - datetime.timedelta(days=1)

    translated_warndate = warn_date.strftime("%A %d %B %Y")

    logging.info(f'warning on {translated_warndate}')
    print(f'warning on {translated_warndate}')

    jobwarn = scheduler.add_job(warn_user, 'date', args=[bst_user], run_date=warn_date,
                                    id=str(bst_user.userid) + ' warn', replace_existing=True, name=f"warn_user {bst_user.username}")
    job = scheduler.add_job(kick_user, 'date', args=[bst_user], run_date=bst_user.subscription,
                                id=str(bst_user.userid), replace_existing=True, name=f"kick_user {bst_user.username}")
    return True


@bot.message_handler(commands=["start", "Start"])
def start(message):
    try:
        userid = message.from_user.id
        # get user object
        bot.send_chat_action(userid, action='typing')

        bst_user = db.User.objects(userid=userid).first()
        # renew = schedule_renew(bst_user)

        if bst_user is None:
            username = message.from_user.username
            # create new user
            bst_user = db.User(
                userid=userid,
                username=username
            )
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
            if data['productid'] is None:
                return bot.send_message(userid, text=data['msg'])
            if data['productid']:
                bot.send_message(userid, text=f"{data['msg']}")
            bot.send_chat_action(userid, action='typing')
            bot.send_message(userid, text='Processing ...')

            productid = data['productid']
            ordername = data['ordername']
            subscribedto = bst_user.subscribed_to(
                productid, orderid)
            translated_subscribedto = subscribedto.strftime("%A %d %B %Y")

            access = asyncio.run(grant_access(bst_user))
            renew = schedule_renew(bst_user)
                
            if orderid != 101010:
                bst_user.orders.append(orderid)
                bst_user.save()

            answer = description["subscription_started"].format(username=username, ordername=ordername, subscribedto=translated_subscribedto, environment=environment)
            join_channel_markup = telebot.types.InlineKeyboardMarkup()
            join_channel_button = telebot.types.InlineKeyboardButton(
                text="Join Now ✅", url=channel_link, callback_data="join_channel")
            join_channel_markup.add(join_channel_button)
        else:
            answer = f"Order number {orderid} has already been used"
            join_channel_markup = None

        bot.send_message(userid, text=answer, reply_markup=join_channel_markup)
    
    except Exception as e:
        print('an error has occurred', e)
        logging.error(e)


@bot.callback_query_handler(func=lambda call: call.data == "join_channel")
def join_channel(call):
    user_id = call.from_user.id
    message_id = call.message.message_id
    pass
