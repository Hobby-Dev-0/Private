from pyrogram import filters 
from DeulexClient import DeulexClient, setbot , vr, Adminsettings
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton , InlineQuery ,Message, CallbackQuery, InlineQueryResultArticle,InputTextMessageContent
__MODULE__ = "Repo"
__HELP__ = """**This command helps you to Repo**
-> `repo`
"""


@DeulexClient.on_message(filters.user(Adminsettings) & filters.command("repo", vr.get("HNDLR")))
async def hikjbhgakd(_, message):
  booet= await setbot.get_me()
  res=await DeulexClient.get_inline_bot_results(booet.username, "repo")
  mg= await DeulexClient.send_inline_bot_result(message.chat.id, res.query_id, res.results[0].id)
  message.delete()
@setbot.on_inline_query(filters.regex("repo"))
async def ibnrp(_ , inline_query):
  stosen= InputTextMessageContent(message_text=f"ððð© ð®ð¤ðªð§ð¨ðð¡ð ð ð ðð£ð ðªð¨ðð§ðð¤ð©\n ð¿ððâð¡ ð¦ðððð  ðâððð")
  keboard= InlineKeyboardMarkup(
                  [  [
                        InlineKeyboardButton(
                            "ð¥Repo",
                            url= "https://github.com/Deulex-Userbot/Deulex"
                        )
                      ]])
  await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Feel like a king",
                input_message_content=stosen,
                thumb_url="https://telegra.ph/file/d19f785fb32bf4eaa62fd.jpg",
                reply_markup=keboard,
            ),
        ]
    )
