import logging
import re
import asyncio

logger = logging.getLogger(__name__)

NEWLINE = "\r\n"

MSG_RE = re.compile(r"""
    # Get the IRCv3 prefix
    # TODO: Parse tags properly
    (?:(?P<tags>@[+A-Za-z0-9.\-:/=;]+)\ +)?
    # Get the "nick!user@host" prefix
    (?:
        # nick
        :(?P<nick>[A-Za-z0-9.\-:_]+)
        # optional user@host
        (?:
            !(?P<user>[^ \x00\r\n]+)
            @(?P<host>[A-Za-z0-9.\-:/]+)
        )?
        \ +
    )?
    # Get command
    (?P<command>[A-Za-z0-9]+)
""", re.VERBOSE)
TRAILING_RE = re.compile(" +:([^\x00\r\n]*)")
PARAM_RE = re.compile(" +([^ \x00\r\n]*)")


class Message:
    __slots__ = ["nick", "user", "host", "command", "params", "tags", "raw"]

    def __init__(self, nick=None, user=None, host=None, command=None, params=None, tags=None, raw=None):
        self.command = command or ""
        self.nick = nick or ""
        self.user = user or ""
        self.host = host or ""
        self.params = params or []
        self.tags = tags or ""
        self.raw = raw or ""

    @property
    def content(self):
        if self.command != "PRIVMSG":
            return None
        return self.params[1]

    @property
    def channel(self):
        if self.command != "PRIVMSG":
            return None
        return self.params[0]

    @classmethod
    def parse(cls, s):
        raw = s
        m = MSG_RE.match(s)
        tags = m.group("tags")
        nick = m.group("nick")
        user = m.group("user")
        host = m.group("host")
        command = m.group("command")
        s = s[m.end():]

        # Get params
        params = []
        while s:
            # Check if we've found the trailing param
            m = TRAILING_RE.match(s)
            # If so, add to the list of params and stop looking for new params
            if m:
                params.append(m.group(1))
                break

            # If not, check if we've found a regular param
            m = PARAM_RE.match(s)
            # If not, then we're done matching params
            if not m:
                break

            # If we've found a param, add it to the list and move forward in the string
            params.append(m.group(1))
            s = s[m.end():]

        # Create the message
        msg = Message(nick, user, host, command, params, tags, raw)
        return msg

    def __str__(self):
        if self.command == "PRIVMSG":
            return f"[{self.channel}] {self.nick}: {self.content}"
        return f"{self.raw}"


class IRC:
    __slots__ = ["nick", "_reader", "_writer", "_readbuffer"]

    def __init__(self, nick):
        self.nick = nick
        self._reader, self._writer = None, None
        self._readbuffer = b""

    async def connect(self, server, port, *, password=None):
        self._reader, self._writer = await asyncio.open_connection(server, port)
        if password is not None:
            await self._send(f"PASS {password}")
        await self._send(f"NICK {self.nick}")

    async def join(self, channel):
        await self._send(f"JOIN {channel}")

    async def readmsg(self):
        msgbytes = await self._reader.readuntil(b"\r\n")
        msgbytes = msgbytes[:-2]

        # Parse the message string into a Message object
        msgstr = str(msgbytes, "utf-8")
        msg = Message.parse(msgstr)
        logger.debug(f"> {msg}")

        # Automatically handle PINGs
        if msg.command == "PING":
            await self.pong()

        return msg

    async def send(self, channel, message):
        await self._send(f"PRIVMSG {channel} :{message}")
        logger.debug(f"< [{channel}]: {message}")

    async def pong(self):
        await self._send("PONG")

    async def _send(self, s):
        self._writer.write(f"{s}\r\n".encode())
        await self._writer.drain()
