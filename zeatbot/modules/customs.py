import logging

import arrow
import toml

from zeatbot import conf
from zeatbot.lib.utils import removeprefix

logger = logging.getLogger("zeatbot")

baked_cmds = [
    "add",
    "remove",
    "say",
    "weather"
]


def on_message(irc, message):
    try_customs(irc, message)
    if message.content.startswith(f"{conf.prefix}add"):
        args = removeprefix(message.content, f"{conf.prefix}add").strip()
        add(irc, args)


def do_replacements(s, message):
    now = arrow.now()
    s = s.replace("%n", message.nick)
    s = s.replace("%s", conf.streamername)
    s = s.replace("%t", now.format("hh:mm"))
    s = s.replace("%d", now.format("YYYY-MM-DD"))
    return s


def try_customs(irc, message):
    cmd = removeprefix(message.content, conf.prefix).split()[0]
    if cmd in baked_cmds:
        return
    customsfile = conf.customsfile
    try:
        customs = toml.load(customsfile)
    except FileNotFoundError:
        logger.warn("Commands file not found. Making a blank one.")
        with open(customsfile) as f:
            f.write("[commands]\r\n")
        return
    for k, v in customs["commands"].items():
        if k == cmd:
            irc.sendmsg(do_replacements(v, message))
            return


# Commands.
def add(irc, args):
    newcmd = args.split()[0]
    newout = removeprefix(args, args.split()[0]).strip()
    if not (newcmd and newout):
        irc.sendmsg(f"Invalid {conf.prefix}add command.")
        logger.warn(f"Invalid {conf.prefix}add command: {conf.prefix}add {args}")
        return
    customs = toml.load(conf.customsfile)
    if newcmd in customs or newcmd in baked_cmds:
        irc.sendmsg(f"{newcmd} is already a command!")
        logger.warn(f"Tried to add {newcmd}, but it's already a command!")
        return
    customs["commands"][newcmd] = newout
    with conf.customsfile.open("w") as f:
        toml.dump(customs, f)


def remove(irc, args):
    cmd = args.split()[0]
    if not cmd:
        irc.sendmsg(f"Invalid {conf.prefix}remove command.")
        logger.warn(f"Invalid {conf.prefix}remove command: {conf.prefix}remove {args}")
        return
    customs = toml.load(conf.customsfile)
    if cmd not in customs:
        irc.sendmsg(f"{cmd} is not a command!")
        logger.warn(f"Tried to remove {cmd}, but it's not a command!")
        return
    del customs["commands"][cmd]
    with conf.customsfile.open("w") as f:
        toml.dump(customs, f)
