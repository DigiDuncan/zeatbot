# import json
import logging
import requests

import arrow

from zeatbot import conf
from zeatbot.lib.utils import removeprefix

logger = logging.getLogger("zeatbot")


def on_message(irc, message):
    if message.content.startswith(f"{conf.prefix}weather"):
        city = removeprefix(message.content, f"{conf.prefix}weather").strip()
        logger.info(f"{message.nick} requested weather info {city}.")
        weather(irc, city)
    elif message.content.startswith(f"{conf.prefix}say"):
        saystring = removeprefix(message.content, f"{conf.prefix}say").strip()
        irc.sendmsg(saystring)


# Commands
def weather(irc, city):
    url_string = f"http://api.weatherapi.com/v1/current.json?key={conf.weather_token}&q={city}"
    r_json = requests.get(url_string).json()
    if "error" in r_json:
        irc.sendmsg(f"{city} is not a valid location.")
        logger.info(f"Didn't send weather info for {city}.")
        return
    loc = r_json["location"]
    location = f"{loc['name']}, {loc['region']}, {loc['country']}"
    temptime = loc['localtime'] + " " + loc['tz_id']
    timearrow = arrow.get(temptime, "YYYY-MM-DD H:mm ZZZ")
    time = timearrow.format("DD MMM YYYY") + ", " + timearrow.format("hh:mm") + " (" + timearrow.format("ZZZ") + " time)"
    condition = r_json["current"]["condition"]["text"]
    humidity = f"{r_json['current']['humidity']}%"
    temperature = r_json["current"]["temp_f"]

    irc.sendmsg(f"In {location}, it's {time}. It is {temperature}°F and {condition}. Humidity {humidity}.")
    logger.info(f"Sent weather info for {location}.")
