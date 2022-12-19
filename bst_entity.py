from telethon import TelegramClient
from config import api_hash, api_id
from telethon.sessions import StringSession


entity_client = TelegramClient(
    StringSession('1BJWap1wBu5DnX3RF528JQ1lsH611GbceEgzaZ3Iz9Q-E_LoE8ErYCH5njzSpnADZY99Pl1QeaHTkLoNxDbWATdrl8LNa1pdJv6H_pGGQ-T0Opb63FalNL2KBhoLylRwPD7ogzzOCdzYw4fxk6A-w4FRXxY-RhtqxWHsNE3pS0N3cx0lO-B0Qlc4dgX8GZmfHPFIm4AoXy_wWNhdl4K9PEFbkoHJr0bVnvwy1o-DMrwLyRk8BkJ1HmB3n8NvDLbFwHFBWuHc9QxvA7DsislPh87h6aOgiXnV9p8vYJkRiuaQfJNQOK88PpOf5wvUu98q3P4ruh8ZVGpMDcnVNfbOY55OlXSb4cQY='), api_id, api_hash)

# entity_client = TelegramClient(
#     'b0t', 1347918, '5681581438678d9390cd4f67ee764f82')


async def get_bst_entity(user_id):
    # Getting user entity via id
    user = await entity_client.get_entity(user_id)
    return user

async def print_all():
        # You can print all the dialogs/conversations that you are part of:
    async for dialog in entity_client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    

entity_client.start()
entity_client.loop.run_until_complete(print_all())
