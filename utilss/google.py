from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from DeulexClient import DeulexClient, vr ,Adminsettings
__MODULE__ = "GOOGLE SEARCH"
__HELP__ = """
__**This command helps you to get to 10 results from google**__
──「 **Usage** 」──
-> `gs`
"""
import requests
from bs4 import BeautifulSoup
from googlesearch import search
def googlesearch(query):
    co=1
    returnquery={}
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        url=str(j)
        response = requests.get(url)
        soup = BeautifulSoup(response.text , 'html.parser')
        metas = soup.find_all('meta')
        site_title=None
        for title in soup.find_all('title'):
            site_title=title.get_text()
        metadeta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
        returnquery[co]={"title":site_title , "metadata":metadeta , "url":j}
        co=co+1
    return returnquery

@DeulexClient.on_message(filters.command("gs",vr.get("HNDLR")) & filters.user(Adminsettings))  
async def gs(_, message):

    msg_txt=message.text 
    returnmsg=""
    query=None
    if " " in msg_txt:
        query=msg_txt[msg_txt.index(" ")+1:len(msg_txt)]
    else:
        await message.reply("Give a query to search")
        return
    results=googlesearch(query)
    for i in range(1,10,1):
        presentquery=results[i]
        presenttitle=presentquery["title"]
        presentmeta=presentquery["metadata"]
        presenturl=presentquery["url"]
        print(presentquery)
        print(presenttitle)
        print(presentmeta)
        print(presenturl)
        if not presentmeta:
            presentmeta=""      
        else:
            presentmeta=presentmeta[0]
        returnmsg=returnmsg+f"[{str(presenttitle)}]({str(presenturl)})\n{str(presentmeta)}\n\n"
    await message.reply(returnmsg)


