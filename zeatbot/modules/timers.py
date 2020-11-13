import logging
import random
import asyncio

from zeatbot import conf
from zeatbot.lib.utils import errlogger

logger = logging.getLogger("zeatbot")


def getTimedMessages():
    try:
        messages = conf.timersfile.read_text(encoding="utf-8").splitlines()
    except EnvironmentError:
        raise Exception("Couldn't load timers file! Ignoring.")
    return messages


@errlogger
async def loop(irc):
    if conf.timedmessagedelay == 0:
        return
    delay_in_seconds = max(conf.timedmessagedelay, 1) * 60
    timed_messages = getTimedMessages()
    messages_to_send = []
    while True:
        if not messages_to_send:
            logger.info("Out of timers! Refueling.")
            messages_to_send = timed_messages.copy()
            random.shuffle(messages_to_send)
        message = messages_to_send.pop()
        await irc.sendmsg(message)
        logger.info(f"Sent timer {message!r}")
        await asyncio.sleep(delay_in_seconds)
