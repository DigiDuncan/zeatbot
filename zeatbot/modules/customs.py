import importlib.resources as pkg_resources
import logging

import arrow
import toml

import zeatbot.data
from zeatbot import conf
from zeatbot.lib.utils import removeprefix

logger = logging.getLogger("zeatbot")

baked_cmds = [
    "add",
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
    customstext = pkg_resources.read_text(zeatbot.data, "commands.ini")
    customs = toml.loads(customstext)
    for k, v in customs["commands"].items():
        if k == cmd:
            irc.sendmsg(do_replacements(v, message))
            return


# Commands.
def add(irc, args):
    newcmd = args.split()[0]
    newout = removeprefix(args, args.split()[0]).strip()
    if not (newcmd and newout):
        irc.sendmsg("Invalid !add command.")
        logger.warn(f"Invalid !add command: !add {args}")
        return
    customstext = pkg_resources.read_text(zeatbot.data, "commands.ini")
    customs = toml.loads(customstext)
    if newcmd in customs or newcmd in baked_cmds:
        irc.sendmsg(f"{newcmd} is already a command!")
        logger.warn(f"Tried to add {newcmd}, but it's already a command!")
        return
    customs[newcmd] = newout
    with open(pkg_resources.open_text(zeatbot.data, "commands.ini")) as f:
        f.write(toml.dumps(customs))
