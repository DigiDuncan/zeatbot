# zeatbot
# by DigiDuncan
# http://github.com/DigiDuncan/zeatbot

import importlib.resources as pkg_resources
import logging
import threading
from pathlib import Path

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

    irc = IRC(oauth = conf.oauth, streamername = conf.streamername,
              botname = conf.botname, displayname = conf.displayname)
    irc.connect()
    irc.sendmsg("I'm online!")
    logger.info(f"Connected to IRC channel #{conf.streamername} as {conf.botname}.")

    def on_message():
        message = irc.readmsg()
        logger.info(message)
        if (message.command == "PING"):
            irc.pong()
        elif message.command == "PRIVMSG":
            baked.on_message(irc, message)
            customs.on_message(irc, message)

    threading.Thread(name="on_message", target=on_message, daemon=True).start()
    # threading.Thread(name="timers", target=timers.loop(irc, conf.timedmessagedelay), daemon=True).start()
