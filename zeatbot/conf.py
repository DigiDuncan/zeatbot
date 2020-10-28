import importlib.resources as pkg_resources

import toml

import zeatbot.data

confpath = pkg_resources.read_text(zeatbot.data, "settings.ini")

prefix = None
botname = None
streamername = None
displayname = None
timedmessagedelay = None


def load():
    global prefix, botname, streamername, displayname, timedmessagedelay
    configDict = toml.load(confpath)
