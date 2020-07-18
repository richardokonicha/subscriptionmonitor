from config import bot, wcapi
import re
from database import BstPage

def get_order(load):
    data = wcapi.get(f"orders/{load}").json()
    return data



@bot.message_handler(commands=["start", "Start"])
def start(message):
    user_id = message.from_user.id
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
        bot.send_message(user_id, text=answer)
    except:
        name = message.from_user.first_name
        bot.send_message(user_id, text=f"this is my father's house {name} Your query parameter is {load}")


