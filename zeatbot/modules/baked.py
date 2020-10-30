# import json
import requests

from zeatbot import conf


def on_message(irc, message):
    if message.content.starts_with("{conf.prefix}weather"):
        city = message.content.remove_prefix("{conf.prefix}weather").strip()
        weather(irc, city)


# Commands
def weather(irc, city):
    url_string = f"http://api.weatherapi.com/v1/current.json?key={conf.weather_token}&q={city}"
    r_json = requests.get(url_string)
    if r_json["error"]:
        irc.sendmsg(f"{city} is not a valid location.")
        return
    loc = r_json["location"]
    location = f"{loc['name']}, {loc['region']}, {loc['country']}"
    time = loc['localtime']
    condition = r_json["current"]["condition"]["text"]
    humidity = f"{r_json['current']['humidity']}%"
    temperature = r_json["current"]["temp_f"]

    irc.sendmsg(f"In {location}, it's {time}. It is {temperature}°F and {condition}. Humidity {humidity}.")
