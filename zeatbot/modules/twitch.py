import logging

import arrow
import twitch

from zeatbot import conf
from zeatbot.lib.utils import removeprefix

logger = logging.getLogger("zeatbot")


async def on_message(irc, client: twitch.TwitchClient, channel: twitch.resources.Channel, message):
    if message.content.startswith(f"{conf.prefix}title"):
        if message.user != conf.streamername:
            await irc.sendmsg("You are not allowed to use this command!")
            return
        title = removeprefix(message.content, f"{conf.prefix}title").strip()
        logger.info(f"{message.nick} changed title to {title}.")
        await streamtitle(irc, client, channel, title)
    if message.content.startswith(f"{conf.prefix}gamename"):
        if message.user != conf.streamername:
            await irc.sendmsg("You are not allowed to use this command!")
            return
        name = removeprefix(message.content, f"{conf.prefix}gamename").strip()
        logger.info(f"{message.nick} changed game name to {name}.")
        await gamename(irc, client, channel, name)
    if message.content.startswith(f"{conf.prefix}uptime"):
        logger.info(f"{message.nick} requested the uptime.")
        await uptime(irc, client, channel)


async def streamtitle(irc, client, channel, title: str):
    client.channels.update(channel.id, status = title)
    logger.info(f"Updating title to {title!r}")


async def gamename(irc, client, channel, name: str):
    client.channels.update(channel.id, game = name)
    logger.info(f"Updating game to {name!r}")


async def uptime(irc, client, channel):
    stream = client.streams.get_stream_by_user(channel.id)
    if stream is None:
        await irc.sendmsg("You're not streaming 4Head")
        return
    await irc.sendmsg("This stream started " + arrow.get(stream.created_at).humanize())
