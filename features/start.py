from config import bot, wcapi
import re
from database import BstPage
import database as db

def get_order(load):
    data = wcapi.get(f"orders/{load}").json()
    return data

@bot.message_handler(commands=["start", "Start"])
def start(message):
    userid = message.from_user.id

    # get user object
    bst_user = db.User.objects(userid=userid).first()
    if bst_user==None:
        username = message.from_user.username if message.from_user.username != " " else message.from_user.first_name
        # create new user
        bst_user = db.User(
            userid=userid,
            username=username
            )
        bst_user.save()

    text = message.text
    load = text.strip("/start ")
    try:
        orderid = int(load)
        # checks if orderid has been used
        checkorder = db.Users.objects(orders=orderid)
        if checkorder == None:
            data = get_order(load)

            productid = data['line_items'][0]['product_id']
            ordername = data['line_items'][0]['name']

            # adds product subscribtion days and stores the order number
            bst_user.subscribed_to(productid, orderid)

            answer = f"""
Hello {name},
Your subscription for {ordername} has been processed
"""
        else:
            answer = f"""Order number {orderid} has already been used"""

        bot.send_message(userid, text=answer)
    except:
        name = message.from_user.first_name
        text = f"Hello {username} Please purchase a plan for bst website to join the VIP group"
        bot.send_message(userid, text=text)



