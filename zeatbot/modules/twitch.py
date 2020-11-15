import logging

import arrow

from twitchplus import streamer_only

logger = logging.getLogger("zeatbot")


def register(bot):
    @bot.command
    @streamer_only(message="You are not allowed to use this command!")
    async def title(msg):
        title = msg.fullargs
        msg.channel.update(status=title)
        logger.info(f"Updating title to {title!r}")
        logger.info(f"{msg.nick} changed title to {title}.")

    @bot.command
    @streamer_only("You are not allowed to use this command!")
    async def gamename(msg):
        name = msg.fullargs
        logger.info(f"{msg.nick} changed game name to {name}.")
        msg.channel.update(game=name)
        logger.info(f"Updating game to {name!r}")

    @bot.command
    async def uptime(msg):
        logger.info(f"{msg.nick} requested the uptime.")
        stream = await msg.get_stream()
        if stream is None:
            await msg.reply("You're not streaming 4Head")
            return
        await msg.reply("This stream started " + arrow.get(stream.created_at).humanize())
