import asyncio
from functools import wraps
import logging

from twitch import TwitchClient

from twitchplus.irc import IRC
from twitchplus.models import Channel, Message, Stream, User

logger = logging.getLogger(__name__)


def errwrapper(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            await fn(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
    return wrapper


def streamer_only(message=None):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(msg):
            if msg.nick != msg.channel.removeprefix("#"):
                return
            return await fn(msg)
        return wrapper
    if callable(message):
        fn = message
        message = None
        return decorator(fn)
    return decorator


class Bot():
    __slots__ = ["nick", "prefix", "irc", "twapi", "_handlers", "_commands", "_user_ids"]

    def __init__(self, nick, prefix=""):
        self.nick = nick
        self.prefix = prefix
        self.irc = None
        self.twapi = None
        self._handlers = {}
        self._commands = {}
        self._user_ids = {}

    async def connect(self, clientid, token, channels=None):
        self.irc = IRC(self.nick)
        await self.irc.connect("irc.twitch.tv", 6667, password=f"oauth:{token}")
        self.twapi = TwitchClient(client_id=clientid, oauth_token=token)
        if channels:
            for c in channels:
                await self.join(c)

    async def join(self, channel):
        await self.irc.join(f"#{channel}")

    async def _runner(self, clientid, token, channels=None):
        await self.connect(clientid, token, channels)
        self._dispatch_on_ready()
        while True:
            irc_msg = await self.irc.readmsg()
            if irc_msg.command != "PRIVMSG":
                continue
            msg = Message.from_irc(self, irc_msg)
            self._dispatch_on_message(msg)
            self._dispatch_command(msg)

    def run(self, clientid, token, channels=None):
        asyncio.run(self._runner(clientid, token, channels))

    def _add_handler(self, event, fn):
        if event not in self._handlers:
            self._handlers[event] = []
        if fn in self._handlers[event]:
            return
        self._handlers[event].append(fn)

    def _add_command(self, name, fn):
        if name in self._commands:
            raise ValueError(f"{name!r} command already exists")
        self._commands[name] = fn

    def _dispatch_on_ready(self):
        for fn in self._handlers["on_ready"]:
            asyncio.create_task(errwrapper(fn)())

    def _dispatch_on_message(self, msg):
        for fn in self._handlers["on_message"]:
            asyncio.create_task(errwrapper(fn)(msg))

    def _dispatch_command(self, msg):
        if not msg.content.startswith(self.prefix):
            return
        try:
            cmd, fn = next((cmd, fn) for cmd, fn in self._commands.items() if msg.content.startswith(self.prefix + cmd))
        except StopIteration:
            return
        msg.prefix = self.prefix
        msg.command = cmd
        msg.fullargs = msg.content.removeprefix(self.prefix + cmd).strip()
        msg.args = msg.fullargs.split()
        asyncio.create_task(errwrapper(fn)(msg))

    def command(self, name=None):
        """command decorator"""
        if callable(name):
            fn = name
            self._add_command(fn.__name__, fn)
            return fn

        def command_deco(fn):
            nonlocal name
            if name is None:
                name = fn.__name__
            self._add_command(fn.__name__, fn)
            return fn

        return command_deco

    def on_message(self, fn):
        """on_message decorator"""
        self._add_handler("on_message", fn)
        return fn

    def on_ready(self, fn):
        """on_ready decorator"""
        self._add_handler("on_ready", fn)
        return fn

    def get_user_id(self, name):
        if name not in self._user_ids:
            (userjson,) = self.twapi.users.translate_usernames_to_ids([name])
            user = User.from_json(self, userjson)
            self._user_ids[name] = user.id
        return self._user_ids[name]

    def get_user(self, name):
        userid = self.get_user_id(name)
        userjson = self.tawpi.users.get_by_id(userid)
        user = User.from_json(self, userjson)
        self._user_ids[user.name] = user.id
        return user

    def get_channel(self, name):
        userid = self.get_user_id(name)
        channeljson = self.twapi.channels.get_by_id(userid)
        channel = Channel.from_json(self, channeljson)
        return channel

    def get_stream(self, name):
        userid = self.get_user_id(name)
        streamjson = self.twapi.streams.get_stream_by_user(userid)
        stream = Stream.from_json(self, streamjson)
        return stream

    async def send(self, channel, content):
        await self.irc.send(f"#{channel}", content)
