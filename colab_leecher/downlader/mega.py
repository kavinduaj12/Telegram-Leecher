import logging
from datetime import datetime
from colab_leecher.utility.helper import status_bar
from colab_leecher.utility.variables import BotTimes, Messages, Paths
from pymegatools import Megatools, MegaError

async def megadl(link: str, num: int):
    global BotTimes
    BotTimes.task_start = datetime.now()
    mega = Megatools()
    try:
        await mega.async_download(link, progress=pro_for_mega, path=Paths.down_path)
    except MegaError as e:
        logging.error(f"An Error occurred: {e}")

async def pro_for_mega(stream, process):
    line = stream[-1]
    file_name = "N/A"
    percentage = 0
    downloaded_size = "N/A"
    total_size = "N/A"
    speed = "N/A"
    try:
        parts = line.split(":")
        file_name = parts[0].strip()
        ok = parts[1].split()
        percentage = float(ok[0][:-1])
        downloaded_size = " ".join(ok[2:4])
        total_size = " ".join(ok[7:9])
        speed = " ".join(ok[9:11])
    except Exception as e:
        logging.error(f"Error parsing status line: {e}")
    Messages.download_name = file_name
    Messages.status_head = f"<b>📥 DOWNLOADING FROM MEGA » </b>\n\n<b>🏷️ Name » </b><code>{file_name}</code>\n"
    
    await status_bar(
        Messages.status_head,
        speed,
        percentage,
        "🤷‍♂️ !!", # TODO: Calculate ETA
        downloaded_size,
        total_size,
        "Meg 😡",
    )
