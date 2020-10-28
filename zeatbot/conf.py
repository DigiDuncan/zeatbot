import importlib.resources as pkg_resources

import toml

import zeatbot.data
from zeatbot.lib import utils

confpath = pkg_resources.read_text(zeatbot.data, "settings.ini")

prefix = None
botname = None
streamername = None
displayname = None
timedmessagedelay = None


def load():
    global prefix, botname, streamername, displayname, timedmessagedelay
    configDict = toml.load(confpath)

    if utils.hasPath(configDict, "settings.prefix"):
        prefix = utils.getPath(configDict, "settings.prefix")
    if utils.hasPath(configDict, "settings.botname"):
        botname = utils.getPath(configDict, "settings.botname")
    if utils.hasPath(configDict, "settings.streamername"):
        streamername = utils.getPath(configDict, "settings.streamername")
    if utils.hasPath(configDict, "settings.displayname"):
        displayname = utils.getPath(configDict, "settings.displayname")
    if utils.hasPath(configDict, "settings.timedmessagedelay"):
        timedmessagedelay = utils.getPath(configDict, "settings.timedmessagedelay")


# Force load when the module loads.
load()
