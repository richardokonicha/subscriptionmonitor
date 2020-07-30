from config import bot, wcapi, scheduler
import re
from database import BstPage
import database as db
from telethon_client import bot as client_bot, main, kick
# from utils import cll
import asyncio


def get_order(load):
    data = wcapi.get(f"orders/{load}").json()
    return data


def kick_user(user):
    user_id = user.id
    client_bot.loop.run_until_complete(kick(user_id))


def set_user_bst(user):
    subscription = user.subscription
    user_id = user.id

    client_bot.start()
    client_bot.loop.run_until_complete(main(user_id))
    scheduler.add_job(kick_user, 'date', run_date=subscription,
                      id=user_id, args=(user))


@bot.message_handler(commands=["start", "Start"])
def start(message):
    userid = message.from_user.id

    # get user object
    bst_user = db.User.objects(userid=userid).first()
    if bst_user == None:
        username = message.from_user.username if message.from_user.username != " " else message.from_user.first_name
        # create new user
        bst_user = db.User(
            userid=userid,
            username=username
        )
        bst_user.save()
    else:
        username = bst_user.username

    text = message.text

    load = re.match("(/start )([0-9]+)", text).groups()[1]

    orderid = int(load)
    # checks if orderid has been used
    checkorder = db.User.objects(orders=orderid)
    if bool(checkorder) == False:
        data = get_order(orderid)

        # adds orderid to list of orders
        # bst_user.orders.append(orderid)
        # bst_user.save()

        productid = data['line_items'][0]['product_id']
        ordername = data['line_items'][0]['name']

        # adds product subscribtion days and stores the order number
        subscribedto = bst_user.subscribed_to(
            productid, orderid).strftime("%A %d %B %Y")
        # if user not in group:
        set_user_bst(bst_user)
        #     update_warning()
        # else:
        #     update_warning()

        answer = f"""
Hello {username},
Your subscription for {ordername} has been processed
Your subscription expires {subscribedto}
"""
    else:
        answer = f"""Order number {orderid} has already been used"""

    bot.send_message(userid, text=answer)

    # except:
    #     username = message.from_user.first_name
    #     text = f"Hello {username} Please purchase a plan for bst website to join the VIP group"
    #     bot.send_message(userid, text=text)
