

@client.route("/yy", method=["POST"])
def purchase_webhook():
    response = response
    response["user"]
    response["subscribtion"]

# telethon send

webhook = [
        {
            "user": "reechee",
            "telegram_link": "ksjfjldsfjreechee@gmali.com",
            "subscribtion": "gold"
        },
        {
            "user": "chizi",
            "telegram_link": "ksjfjldsfjchizy@gmali.com",
            "subscribtion": "premuim"
        },
        {
            "user": "nzeako",
            "telegram_link": "ksjfjldsfjnzeako@gmali.com",
            "subscribtion": "silver"
        },
]

if user.status == 'newuser':
    if webhook["subscription"] == gold:
        expire_date = datetime.datetime.now() + 20
        db.user.expire_date=expire_date
        db.user.commit()
if user.status == 'regular':
    now = datatime.datetime.now()
    warndate = expire_date-10

    if now >= warndate and user.warn==False:
        telethon.speak('Your subscription has almost finished, be warned')
        user.warn = True
        
    if now >= expire_date and user.warn ==True:
        telethon.speak('Your subscription has expired. Please renew your subscription to continue')
        telethon.remove_user()

        