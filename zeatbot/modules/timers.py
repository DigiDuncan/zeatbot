import logging
import random
import time

from zeatbot import conf

logger = logging.getLogger("zeatbot")

try:
    with open(conf.timersfile) as f:
        timers = f.readlines()
except EnvironmentError:
    logger.error("Couldn't load timers file! Ignoring.")
    timers = None

currentpool = timers


def loop(irc, minutes):
    global currentpool

    if currentpool is None:
        return
    message = currentpool.pop(random.choice(len(currentpool) - 1))
    irc.sendmsg(message)
    logger.info(f"Sent timer {message!r}")
    if currentpool == []:
        logger.info("Out of timers! Refueling.")
        currentpool = timers
    time.sleep(minutes * 60)
