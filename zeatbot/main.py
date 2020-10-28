# zeatbot
# by DigiDuncan
# http://github.com/DigiDuncan/zeatbot

import logging
from digiformatter import logger as digilogger

# Set up logging
logging.basicConfig(level=logging.INFO)
dfhandler = digilogger.DigiFormatterHandler()

logger = logging.getLogger("zeatbot")
logger.handlers = []
logger.propagate = False
logger.addHandler(dfhandler)
