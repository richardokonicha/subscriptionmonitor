from telethon import TelegramClient
from config import api_hash, api_id, sessionString
from telethon.sessions import StringSession


entity_client = TelegramClient(
    StringSession(sessionString), api_id, api_hash)

# entity_client = TelegramClient(
#     'anon', api_id, api_hash)


async def get_bst_entity(user_id):
    # Getting user entity via id
    user = await entity_client.get_entity(user_id)
    return user

# entity_client.start()
# entity_client.loop.run_until_complete(get_bst_entity(
#     ""))
