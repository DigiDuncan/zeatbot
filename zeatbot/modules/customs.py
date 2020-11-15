import logging

import arrow
import toml

from twitchplus import streamer_only
from zeatbot import conf
from zeatbot.lib.utils import removeprefix

logger = logging.getLogger("zeatbot")

baked_cmds = [
    "add",
    "remove",
    "say",
    "weather"
]

def load_customs():
    try:
        customs = toml.loads(conf.customsfile.read_text())
    except FileNotFoundError:
        customs = {"commands": {}}
    return customs

def save_customs(customs):
    conf.customsfile.write_text(toml.dumps(customs))

def register(bot):
    @bot.on_message
    async def try_customs(msg):
        cmd = removeprefix(msg.content, conf.prefix).split()[0]
        if cmd in baked_cmds:
            return
        customs = load_customs()
        for k, v in customs["commands"].items():
            if k == cmd:
                await msg.reply(do_replacements(v, msg.nick))
                return

    @bot.command
    @streamer_only
    async def add(msg):
        newcmd = msg.args[0]
        newout = removeprefix(msg.fullargs, newcmd).strip()
        if not (newcmd and newout):
            await msg.reply(f"Invalid {conf.prefix}add command.")
            logger.warn(f"Invalid {conf.prefix}add command: {msg.content}")
            return
        customs = load_customs()
        if newcmd in customs["commands"] or newcmd in baked_cmds:
            await msg.reply(f"{newcmd} is already a command!")
            logger.warn(f"Tried to add {newcmd}, but it's already a command!")
            return
        customs["commands"][newcmd] = newout
        save_customs(customs)

    @bot.command
    @streamer_only
    async def remove(msg):
        cmd = msg.args[0]
        if not cmd:
            await msg.reply(f"Invalid {conf.prefix}remove command.")
            logger.warn(f"Invalid {conf.prefix}remove command: {msg.content}")
            return
        customs = load_customs()
        if cmd not in customs["commands"]:
            await msg.reply(f"{cmd} is not a command!")
            logger.warn(f"Tried to remove {cmd}, but it's not a command!")
            return
        del customs["commands"][cmd]
        save_customs(customs)


def do_replacements(s, nick):
    now = arrow.now()
    s = s.replace("%n", nick)
    s = s.replace("%s", conf.streamername)
    s = s.replace("%t", now.format("hh:mm"))
    s = s.replace("%d", now.format("YYYY-MM-DD"))
    return s
