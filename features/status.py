from config import bot, wcapi, scheduler
import re
import database as db
import datetime
from config import join_channel_markup


@bot.message_handler(commands=["status", "Status"])
def status(message):
    userid = message.from_user.id
    bst_user = db.User.objects(userid=userid).first()
    if bst_user == None:
        answer = "You have no subscription"
        return bot.send_message(userid, text=answer)
    else:
        expireSub = bst_user.subscription
        now = datetime.datetime.now()

        if expireSub >= now:
            expire = bst_user.subscription.strftime("%A %d %B %Y")
            answer = f"Your plan will expire on {expire}"
            markup = join_channel_markup
        else:
            answer = "Sorry, your subscription has expired"
            markup = None

        return bot.send_message(userid, text=answer, reply_markup=markup)
