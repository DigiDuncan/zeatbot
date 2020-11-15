import logging
from base64 import b64decode
from pathlib import Path

import appdirs
import toml

from zeatbot.lib import utils

logger = logging.getLogger("zeatbot")


def getDataDir():
    appname = "zeatbot"
    appauthor = "DigiDuncan"
    datadir = Path(appdirs.user_data_dir(appname, appauthor))
    return datadir


datadir = getDataDir()
conffile = datadir / "settings.ini"
customsfile = datadir / "commands.ini"
timersfile = datadir / "timers.txt"
oauthpath = datadir / "authtoken.txt"
clientidpath = datadir / "client_id.txt"

prefix = None
botname = None
streamername = None
displayname = None
timedmessagedelay = None
oauth = None
clientid = None
weather_token = None


def loadline(p: Path):
    try:
        line = p.read_text().splitlines()[0].strip()
    except FileNotFoundError:
        line = ""
    return line


def load():
    global prefix, botname, streamername, displayname, timedmessagedelay
    global oauth, clientid
    global weather_token

    configDict = toml.load(conffile)

    # Settings
    if utils.hasPath(configDict, "settings.prefix"):
        prefix = utils.getPath(configDict, "settings.prefix")
    if utils.hasPath(configDict, "settings.botname"):
        botname = utils.getPath(configDict, "settings.botname")
    if utils.hasPath(configDict, "settings.streamername"):
        streamername = utils.getPath(configDict, "settings.streamername").lower()
    if utils.hasPath(configDict, "settings.displayname"):
        displayname = utils.getPath(configDict, "settings.displayname")
    if utils.hasPath(configDict, "settings.timedmessagedelay"):
        timedmessagedelay = utils.getPath(configDict, "settings.timedmessagedelay", 1)

    # Load bot authtoken
    oauth = loadline(oauthpath)
    if not oauth:
        logger.error("OAuth token not found! Cannot log in.")
        logger.warning(f"Place an authtoken file at {oauthpath}.")

    # Load client ID
    clientid = loadline(clientidpath)
    if not clientid:
        logger.error("Client ID not found! Cannot log in.")
        logger.warning(f"Place an client ID file at {clientidpath}.")

    # Load API authtokens
    if utils.hasPath(configDict, "tokens.weather"):
        weather_token = b64decode(utils.getPath(configDict, "tokens.weather")).decode(encoding="utf-8")
    else:
        logger.error("Weather token missing! Contact DigiDuncan. The weather command will not work.")
