import logging
import random
import asyncio

from zeatbot import conf
from zeatbot.lib.utils import errlogger

logger = logging.getLogger("zeatbot")


def getTimedMessages():
    try:
        with open(conf.timersfile, encoding="utf-8") as f:
            messages = f.readlines()
            for t in messages:
                t = t.strip()
    except EnvironmentError:
        raise Exception("Couldn't load timers file! Ignoring.")
    return messages


@errlogger
async def loop(irc):
    timed_messages = getTimedMessages()
    messages_to_send = []
    while True:
        if not messages_to_send:
            logger.info("Out of timers! Refueling.")
            messages_to_send = timed_messages.copy()
            random.shuffle(messages_to_send)
        message = messages_to_send.pop()
        irc.sendmsg(message)
        logger.info(f"Sent timer {message!r}")
        await asyncio.sleep(conf.timedmessagedelay * 60)
