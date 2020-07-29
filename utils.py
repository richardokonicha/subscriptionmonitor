from telethon import TelegramClient
from dotenv import load_dotenv
import os
load_dotenv
# Remember to use your own values from my.telegram.org!


api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
client = TelegramClient('anon', api_id, api_hash)
client = TelegramClient('anon', 1347918, '5681581438678d9390cd4f67ee764f82')

async def main():
    # Getting information about yourself
    me = await client.get_me()
    print(me.stringify())
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...
    await client.send_message('me', 'Hello, myself!')

client = TelegramClient('anon', 1347918, '5681581438678d9390cd4f67ee764f82')
client.start()
# client.kick_participant
# client.disconnect()