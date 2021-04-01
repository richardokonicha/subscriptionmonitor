
# Remember to use your own values from my.telegram.org!
from telethon.sessions import StringSession
from telethon import TelegramClient, events

api_id = 1271225
api_hash = "f36c296645a468c16a698ecb1e59e31b"
session = ""
# client = TelegramClient('anon', api_id, api_hash)
client = TelegramClient(StringSession(session), api_id, api_hash)


async def main():
    # async for dialog in client.iter_dialogs():
        # print(dialog.name, 'has ID', dialog.id)
    string = client.session.save()
    print(string)


with client:
    client.loop.run_until_complete(main())


#  Illyrian = -1001236662259