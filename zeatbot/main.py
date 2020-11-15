# zeatbot
# by DigiDuncan
# http://github.com/DigiDuncan/zeatbot

import importlib.resources as pkg_resources
import logging
from pathlib import Path

from digiformatter import logger as digilogger

import zeatbot.data
from zeatbot import conf
from zeatbot.modules import baked, customs, timers, twitch

from twitchplus import Bot


# Set up logging
logging.basicConfig(level=logging.DEBUG)
dfhandler = digilogger.DigiFormatterHandler()

logger = logging.getLogger("zeatbot")
logger.handlers = []
logger.propagate = False
logger.addHandler(dfhandler)

asynciologger = logging.getLogger("asyncio")
asynciologger.handlers = []
asynciologger.propagate = False
asynciologger.addHandler(dfhandler)


def main():
    try:
        conf.load()
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e.filename}")
        logger.warn("Writing default settings file...")
        default_settings = pkg_resources.read_text(zeatbot.data, "settings.ini")
        Path(e.filename).parent.mkdir(parents = True, exist_ok = True)
        with open(e.filename, "w") as f:
            f.write(default_settings)
        logger.info("Please reload the bot.")
        return

    bot = Bot(nick=conf.botname, prefix=conf.prefix)
    baked.register(bot)
    customs.register(bot)
    twitch.register(bot)
    timers.register(bot)

    @bot.on_ready
    async def on_ready(): 
        channel = bot.get_channel(conf.streamername)
        logger.info(f"Connected to IRC channel #{conf.streamername} as {conf.botname}.")
        await channel.send("I'm online!")

    bot.run(conf.clientid, conf.oauth, channels=[f"{conf.streamername}"])


if __name__ == "__main__":
    main()
