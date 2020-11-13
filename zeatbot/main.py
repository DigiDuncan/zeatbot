# zeatbot
# by DigiDuncan
# http://github.com/DigiDuncan/zeatbot

import importlib.resources as pkg_resources
import logging
from pathlib import Path
import asyncio

from digiformatter import logger as digilogger
from twitch import TwitchClient

import zeatbot.data
from zeatbot import conf
from zeatbot.lib.irc import IRC
from zeatbot.modules import baked, customs, timers


# Set up logging
logging.basicConfig(level=logging.INFO)
dfhandler = digilogger.DigiFormatterHandler()

logger = logging.getLogger("zeatbot")
logger.handlers = []
logger.propagate = False
logger.addHandler(dfhandler)


async def main():
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

    irc = IRC(oauth = conf.oauth, streamername = conf.streamername,
              botname = conf.botname, displayname = conf.displayname)
    await irc.connect()
    await irc.sendmsg("I'm online!")
    logger.info(f"Connected to IRC channel #{conf.streamername} as {conf.botname}.")

    asyncio.create_task(timers.loop(irc))
    while True:
        message = await irc.readmsg()
        logger.info(message)
        if (message.command == "PING"):
            await irc.pong()
        elif (message.command == "PRIVMSG"):
            asyncio.create_task(on_message(irc, message))


async def on_message(irc, message):
    asyncio.create_task(baked.on_message(irc, message))
    asyncio.create_task(customs.on_message(irc, message))


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
