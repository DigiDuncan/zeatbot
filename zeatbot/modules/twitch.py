import logging

from zeatbot import conf
from zeatbot.lib.utils import removeprefix

logger = logging.getLogger("zeatbot")


async def on_message(irc, client, channel, message):
    if message.content.startswith(f"{conf.prefix}title"):
        if message.user != conf.streamername:
            irc.sendmsg("You are not allowed to use this command!")
            return
        title = removeprefix(message.content, f"{conf.prefix}title").strip()
        logger.info(f"{message.nick} changed title to {title}.")
        await title(irc, channel, title)


async def title(irc, channel, title):
    ...
