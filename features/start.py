from config import bot, wcapi
import re

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
        bot.send_message(user_id, text=f"this is my father's house {name} Your query parameter is {load} and your data is {data}")
    except:
        name = message.from_user.first_name
        bot.send_message(user_id, text=f"this is my father's house {name} Your query parameter is {load}")

