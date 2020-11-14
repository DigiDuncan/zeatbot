# zeatbot
It's a bot for [zeat](http://www.twitch.tv/zeat). It's zeatbot.

## How to Use
Make sure you have [Python 3](https://www.python.org/downloads/) installed. Make sure you installed `pip` with it.

To start run the bot once. It will place a default settings file in the App Directory (On Windows, this is `%LocalAppData%\DigiDuncan\zeatbot`, on Linux it's (usually?) `~/.local/share/zeatbot`.)
Place a file called `authtoken.txt` in the App Directory. This file should only contain a Twitch authtoken, and should look something like this:
```
0123456789abcdefghijABCDEFGHIJ
```
Place another file in the same location called `client_id.txt`. This file should contain your Client ID, and should look something like this.
```
0123456789abcdefghijABCDEFGHIJ
```

## Features
* Customizable prefix (defaults to `!`)
* A weather command (`!weather <location>`)
* A say command (`!say <text>`)
* Timed messages every X minutes
* Custom text responses (`!add <command> <response...>` and `!remove <command>`)

### Custom text responses
Custom text responses are loaded from the file `commands.ini` in the App Directory. They are formatted like so:
```ini
[commands]  # This is important!
test = "Boy howdy is this a test!"
test2 = "Hey %n, this is a test!"
test3 = "Wow, I added this baby myself!"
```
To run them, use the prefix and then the name of the command in chat.
Commands will replace the following strings with certain data:
* **%n**: the command runner's name.
* **%s**: the streamer's name.
* **%t**: the current time (HH:MM)
* **%d**: the current date (YYYY-MM-DD)
You can add new commands from either this file, or using `!add command_name command response wee!` and `!remove command_name` to remove it.

### Timers
Timers run every X minutes, sending a message to chat. X is a number specified in `settings.ini`.
To add timers, open up (or create) `timers.txt` in the App Directory. Each new line is a seperate message to send!
