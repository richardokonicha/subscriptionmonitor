from telethon import TelegramClient
from config import api_hash, api_id, bot_sessionString
from telethon.sessions import StringSession


entity_client = TelegramClient(
    StringSession(bot_sessionString), api_id, api_hash)

# entity_client = TelegramClient(
#     'b0t', 1347918, '5681581438678d9390cd4f67ee764f82')


async def get_bst_entity(user_id):
    # Getting user entity via id
    user = await entity_client.get_entity(user_id)
    return user

# entity_client.start()
# entity_client.loop.run_until_complete(get_bst_entity(1159640443))
