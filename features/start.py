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

    text = message.text
    load = text.strip("/start ")
    try:
        load = int(load)
        data = get_order(load)
        # name = [i.name for i in data['line_items']]
        order_name = data['line_items'][0]['name']
        answer = f"""
Hello {name},
Your subscription for {order_name} has been processed

"""
        bot.send_message(userid, text=answer)
    except:
        name = message.from_user.first_name
        bot.send_message(userid, text=f"this is my father's house {name} Your query parameter is {load}")


