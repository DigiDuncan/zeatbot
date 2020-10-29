# zeatbot
# by DigiDuncan
# http://github.com/DigiDuncan/zeatbot

import logging
from digiformatter import logger as digilogger
from zeatbot import conf
from zeatbot.lib.irc import IRC


# Set up logging
logging.basicConfig(level=logging.INFO)
dfhandler = digilogger.DigiFormatterHandler()

logger = logging.getLogger("zeatbot")
logger.handlers = []
logger.propagate = False
logger.addHandler(dfhandler)
