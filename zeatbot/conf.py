import importlib.resources as pkg_resources
import logging
from base64 import b64decode
from pathlib import Path

import toml

import zeatbot.data
from zeatbot.lib import utils

logger = logging.getLogger("zeatbot")

conftext = pkg_resources.read_text(zeatbot.data, "settings.ini")
oauthpath = Path(__file__).resolve().parent.parent / "authtoken.txt"

prefix = None
botname = None
streamername = None
displayname = None
timedmessagedelay = None
oauth = None
weather_token = None


def load():
    global prefix, botname, streamername, displayname, timedmessagedelay, oauth
    global weather_token

    configDict = toml.loads(conftext)

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
        timedmessagedelay = utils.getPath(configDict, "settings.timedmessagedelay")

    # Load bot authtoken
    try:
        with open(oauthpath) as f:
            oauth = f.readline()
    except FileNotFoundError:
        logger.error("OAuth token not found! Cannot log in.")

    # Load API authtokens
    if utils.hasPath(configDict, "tokens.weather"):
        weather_token = b64decode(utils.getPath(configDict, "tokens.weather")).decode(encoding="utf-8")
