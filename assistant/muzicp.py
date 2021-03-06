import ffmpeg
from DeulexClient import vcbot, setbot , Adminsettings
from pytgcalls import GroupCall
import asyncio
import os
import time
import requests
import datetime
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos
from pyrogram import filters
s = []
s_dict = {}
group_call = GroupCall(vcbot, play_on_repeat=False)
__MODULE__ = "VcPlayer"
__HELP__ = """**This command helps you to Vc Player**
-> 'play` `splay` `skip` `next` `pause` `resume` `replay` `stope` `rejoin` `leave` `setvol`
"""

@setbot.on_message(
    filters.command(["play"])
    & filters.group
    & ~ filters.edited
)
async def pl(client, message):
    play = await message.reply_text("`Please Wait!`")
    song = f"**PlayList in {message.chat.title}** \n"
    sno = 0
    if not s:
        if group_call.is_connected:
            await play.edit(f"**Currently Playing :** `{str(group_call.input_filename).replace('.raw', '')}`")
        else:
            await play.edit("`Playlist is Empty Sar And Nothing is Playing Also :(!`")
            return
    if group_call.is_connected:
        song += f"**Currently Playing :** `{str(group_call.input_filename).replace('.raw', '')}` \n\n"
    for i in s:
        sno += 1
        song += f"**{sno} ▶** `{i.replace('.raw', '')} | {s_dict[i]['singer']} | {s_dict[i]['dur']}` \n\n" 
    await play.edit(song)

@group_call.on_playout_ended
async def playout_ended_handler(group_call, filename):
    global s
    client_ = group_call.client
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    if not s:
        await setbot.send_message(
            int(f"-100{group_call.full_chat.id}"),
            f"`Finished Playing. Nothing Left Play! Left VC.`",
        )
        await group_call.stop()
        return
    await client_.send_message(
        int(f"-100{group_call.full_chat.id}"), f"**Now Playing :** `{str(s[0]).replace('.raw', '')} | {s_dict[s[0]]['singer']} | {s_dict[s[0]]['dur']}` \n\n"
    )
    holi = s[0]
    s.pop(0)
    group_call.input_filename = holi

@setbot.on_message(
    filters.command(["skip", "next"])
    & filters.group
    & ~ filters.edited
)
async def ski_p(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return 
    m_ = await message.reply_text("`Please Wait!`")
    no_t_s = get_text(message)
    if not no_t_s:
        return await m_.edit("`Give Me Valid List Key Len.`")
    if no_t_s == "current":
        if not s:
            return await m_.edit("`No Song in List. So Stopping Song is A Smarter Way.`")
        next_s = s[0]
        s.pop(0)
        name = str(next_s).replace(".raw", "")
        prev = group_call.input_filename
        group_call.input_filename = next_s
        return await m_.edit(f"`Skipped {prev}. Now Playing {name}!`")       
    else:
        if not s:
            return await m_.edit("`There is No Playlist.`")
        if not no_t_s.isdigit():
            return await m_.edit("`Input Should Be In Digits.`")
        no_t_s = int(no_t_s)
        if int(no_t_s) == 0:
            return await m_.edit("`0? What?`")
        no_t_s = int(no_t_s - 1)
        try:
            s_ = s[no_t_s]
            s.pop(no_t_s)
        except:
            return await m_.edit("`Invalid Key.`")
        return await m_.edit(f"`Skipped : {s_} At Position #{no_t_s}`")
                            
    
@setbot.on_message(
    filters.command(["splay"])
    & filters.group
    & ~ filters.edited
)
async def play_m(client, message):
    global s
    global s_dict
    u_s = await message.reply_text("`Processing..`")
    if message.reply_to_message:
         if message.reply_to_message.audio:
             await u_s.edit_text("`Please Wait, Let Me Download This File!`")
             audio = message.reply_to_message.audio
             audio_original = await message.reply_to_message.download()
             vid_title = audio.title or audio.file_name
             uploade_r = message.reply_to_message.audio.performer or "Unknown Artist."
             dura_ = message.reply_to_message.audio.duration
             dur = datetime.timedelta(seconds=dura_)
             raw_file_name = f"{audio.file_name}.raw" if audio.file_name else f"{audio.title}.raw"
         else:
             return await u_s.edit("`Reply To A File To PLay It.`")
    else:
         input_str = message.text.split(1)[1]
         if not input_str:
             return await u_s.edit("`Give Me A Song Name. Like Why we lose or Alone.`")
         search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
         rt = search.result()
         try:
             result_s = rt["search_result"]
         except:
             return await u_s.edit(f"`Song Not Found With Name {input_str}, Please Try Giving Some Other Name.`")
         url = result_s[0]["link"]
         dur = result_s[0]["duration"]
         vid_title = result_s[0]["title"]
         yt_id = result_s[0]["id"]
         uploade_r = result_s[0]["channel"]
         opts = {
             "format": "bestaudio",
             "addmetadata": True,
             "key": "FFmpegMetadata",
             "writethumbnail": True,
             "prefer_ffmpeg": True,
             "geo_bypass": True,
             "nocheckcertificate": True,
             "postprocessors": [
                 {
                     "key": "FFmpegExtractAudio",
                     "preferredcodec": "mp3",
                     "preferredquality": "720",
                 }
             ],
             "outtmpl": "%(id)s.mp3",
             "quiet": True,
             "logtostderr": False,
         }
         try:
             with YoutubeDL(opts) as ytdl:
                 ytdl_data = ytdl.extract_info(url, download=True)
         except Exception as e:
             await u_s.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
             return
         audio_original = f"{ytdl_data['id']}.mp3"
         raw_file_name = f"{vid_title}.raw"
    raw_file_name = await convert_to_raw(audio_original, raw_file_name)
    if not raw_file_name:
         return await u_s.edit("`FFmpeg Failed To Convert Song To raw Format. Please Give Valid File.`")
    os.remove(audio_original)
    if not group_call.is_connected:
        try:
            await group_call.start(message.chat.id)
        except BaseException as e:
            return await u_s.edit(f"**Error While Joining VC:** `{e}`")
        group_call.input_filename = raw_file_name
        return await u_s.edit(f"Playing `{vid_title}` in `{message.chat.title}`!")
    else:
        s.append(raw_file_name)
        f_info = {"song name": vid_title,
                  "singer": uploade_r,
                  "dur": dur
                 }
        s_dict[raw_file_name] = f_info
        return await u_s.edit(f"Added `{vid_title}` To Position `#{len(s)+1}`!")
    

      
async def convert_to_raw(audio_original, raw_file_name):
    try:
         ffmpeg.input(audio_original).output(
              raw_file_name, format="s16le", acodec="pcm_s16le", ac=2, ar="48k").overwrite_output().run()
    except:
         return None
    return raw_file_name

 
@setbot.on_message(
    filters.command(["pause"])
    & filters.group
    & ~ filters.edited
)
async def no_song_play(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return    
    await message.reply_text(f"`⏸ Paused {str(group_call.input_filename).replace('.raw', '')}.`")
    group_call.pause_playout()
    
    
@setbot.on_message(
    filters.command(["resume"])
    & filters.group
    & ~ filters.edited
)
async def wow_dont_stop_songs(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return    
    group_call.resume_playout()
    await message.reply_text(f"`▶️ Resumed.`")
        
        
@setbot.on_message(
    filters.command(["stope"])
    & filters.group
    & ~ filters.edited
)
async def kill_vc_(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    group_call.stop_playout()
    await message.reply_text("`Stopped Playing Songs!`")


@setbot.on_message(
    filters.command(["replay"])
    & filters.group
    & ~ filters.edited
)
async def replay(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return
    group_call.restart_playout()
    await message.reply_text(f"`Re-Playing : {group_call.input_filename}`")


@setbot.on_message(
    filters.command(["rejoin"])
    & filters.group
    & ~ filters.edited
)
async def rejoinvcpls(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return
    await group_call.reconnect()
    await message.reply_text(f"`Rejoined! - Vc`")


@setbot.on_message(
    filters.command(["leave"])
    & filters.group
    & ~ filters.edited
)
async def leave_vc_test(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    await group_call.stop()
    await message.reply_text(f"`Left : {message.chat.title} - Vc`")

@setbot.on_message(
    filters.command(["setvol"])
    & filters.group
    & ~ filters.edited
)
async def set_vol(client, message):
    if not group_call.is_connected:
        await message.reply_text("`Is Group Call Even Connected?`")
        return
    volume = get_text(message)
    if not volume:
        await message.reply_text("Volume Should Be Integer!")
        return
    if not volume.isdigit():
        await message.reply_text("Volume Should Be Integer!")
        return
    if int(volume) < 2:
        await message.reply_text("Volume Should Be Above 2")
        return
    if int(volume) >= 100:
        await message.reply_text("Volume Should Be Below 100")
        return
    await group_call.set_my_volume(volume)
    await message.reply_text(f"**Volume :** `{volume}`")

