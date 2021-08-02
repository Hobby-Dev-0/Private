from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from DeulexClient import DeulexClient, vr ,Adminsettings
__MODULE__ = "pin"
__HELP__ = """
__**This command helps you to instantly pin a message in the chat**__
──「 **Usage** 」──
-> `pin`
"""

@DeulexClient.on_message(filters.command("pin",vr.get("HNDLR")) & filters.user(Adminsettings))  
async def pin_message(_, message):
    msg_id=message.message_id
    chat_id=message.chat.id
    if message.reply_to_message == None:
        await DeulexClient.edit_message_text(chat_id , msg_id , "Shall I pin your head to wall ?")
    else:
        if message.chat.type == "private":
            reply_msg_id=message.reply_to_message.message_id
            await DeulexClient.pin_chat_message(chat_id , reply_msg_id , both_sides=True)
            await message.edit_text("Done the Job master !")
        else:
            zuzu= await DeulexClient.get_chat_member(chat_id , "me")
            can_pin=zuzu.can_pin_messages
            if not can_pin:
                await DeulexClient.edit_message_text(chat_id , msg_id , "Not a admin bruh 🥱") 
            else:         
                reply_msg_id=message.reply_to_message.message_id
                await DeulexClient.pin_chat_message(chat_id , reply_msg_id)
                await DeulexClient.edit_message_text(chat_id , msg_id , "Done the Job master !")
