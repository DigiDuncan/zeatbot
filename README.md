# zeatbot
It's a bot for Zeat. It's zeatbot.

## How to Use
Make sure you have [Python 3](https://www.python.org/downloads/) installed.

To start, place a file called `authtoken.txt` in the root directory of this folder (the same folder this `README.md` is in.) This file should only contain a Twitch authtoken, and should look something like this:
```
oauth:0123456789abcdefghijklmnopqrst
```

Included with **zeatbot** is a `run.bat` file in the root directory. If you're Zeat, this has been tailored to you and should "just work." If you're not Zeat, or your forking this repo to make your own bot, you'll need to either change that file to do the equivalent of launching `zeatbot/main.py` as a Python module on your system.

`firsttime.bat` runs a first-time setup, ensuring you have all the required Python packages. You can alsmo do this yourself by installing all the rquirements in `requirements.txt` yourself.
