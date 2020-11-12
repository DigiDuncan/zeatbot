import logging
import random
import time

from zeatbot import conf

logger = logging.getLogger("zeatbot")

try:
    with open(conf.timersfile, encoding="utf-8") as f:
        timers = f.readlines()
        for t in timers:
            t = t.strip()
except EnvironmentError:
    logger.error("Couldn't load timers file! Ignoring.")
    timers = None

currentpool = timers


def loop(irc, minutes):
    while True:
        global currentpool

        if currentpool is None:
            return
        message = currentpool.pop(random.randrange(len(currentpool)))
        irc.sendmsg(message)
        logger.info(f"Sent timer {message!r}")
        if currentpool == []:
            logger.info("Out of timers! Refueling.")
            currentpool = timers
        time.sleep(minutes * 60)
