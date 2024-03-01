import logging
import yt_dlp
from asyncio import sleep
from threading import Thread
from os import makedirs, path as ospath
from colab_leecher.utility.handler import cancelTask
from colab_leecher.utility.variables import YTDL, MSG, Messages, Paths
from colab_leecher.utility.helper import getTime, keyboard, sizeUnit, status_bar, sysINFO

async def send_formats_as_buttons(chat_id, formats):
    markup = telebot.types.InlineKeyboardMarkup()
    for format in formats:
        button = telebot.types.InlineKeyboardButton(text=format, callback_data=format)
        markup.add(button)
    await bot.send_message(chat_id, "Available formats:", reply_markup=markup)

async def YTDL_Status(link, num):
    global Messages, YTDL
    name, formats = await get_YT_Info(link)
    Messages.status_head = f"<b>📥 DOWNLOADING FROM » </b><i>🔗Link {str(num).zfill(2)}</i>\n\n<code>{name}</code>\n"
    
    await send_formats_as_buttons(chat_id, formats)

    YTDL_Thread = Thread(target=YouTubeDL, name="YouTubeDL", args=(link,))
    YTDL_Thread.start()

    while YTDL_Thread.is_alive():  # Until ytdl is downloading
        if YTDL.header:
            sys_text = sysINFO()
            message = YTDL.header
            try:
                await MSG.status_msg.edit_text(text=Messages.task_msg + Messages.status_head + message + sys_text, reply_markup=keyboard())
            except Exception:
                pass
        else:
            try:
                await status_bar(
                    down_msg=Messages.status_head,
                    speed=YTDL.speed,
                    percentage=float(YTDL.percentage),
                    eta=YTDL.eta,
                    done=YTDL.done,
                    left=YTDL.left,
                    engine="Xr-YtDL 🏮",
                )
            except Exception:
                pass

        await sleep(2.5)
