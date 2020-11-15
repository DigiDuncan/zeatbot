# import json
import logging
import requests

import arrow

from twitchplus import streamer_only
from zeatbot import conf

logger = logging.getLogger("zeatbot")


# Commands
def register(bot):
    @bot.command
    @streamer_only
    async def say(msg):
        saystring = msg.fullargs
        await msg.reply(saystring)

    @bot.command
    async def weather(msg):
        city = msg.fullargs
        logger.info(f"{msg.nick} requested weather info {city}.")
        url_string = f"http://api.weatherapi.com/v1/current.json?key={conf.weather_token}&q={city}"
        r_json = requests.get(url_string).json()
        if "error" in r_json:
            await msg.reply(f"{city} is not a valid location.")
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

        await msg.reply(f"In {location}, it's {time}. It is {temperature}°F and {condition}. Humidity {humidity}.")
        logger.info(f"Sent weather info for {location}.")
