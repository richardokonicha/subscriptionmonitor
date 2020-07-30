from config import bot, wcapi, scheduler
import re
import database as db


@bot.message_handler(commands=["status", "Status"])
def status(message):
    userid = message.from_user.id
    bst_user = db.User.objects(userid=userid).first()
    if bst_user == None:
        answer = "You have no subscription"
        return bot.send_message(userid, text=answer)
    else:
        expire = bst_user.subscription.strftime("%A %d %B %Y")
        answer = f"Your plan will expire on {expire}"

        return bot.send_message(userid, text=answer)
