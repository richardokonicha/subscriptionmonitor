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
    else:
        username = bst_user.username

    text = message.text

    try:
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
            subscribedto = bst_user.subscribed_to(productid, orderid).strftime("%Y %B %A %d")

            answer = f"""
Hello {username},
Your subscription for {ordername} has been processed
Your subscription expires {subscribedto}
"""
        else:
            answer = f"""Order number {orderid} has already been used"""

        bot.send_message(userid, text=answer)
    except:
        username = message.from_user.first_name
        text = f"Hello {username} Please purchase a plan for bst website to join the VIP group"
        bot.send_message(userid, text=text)



