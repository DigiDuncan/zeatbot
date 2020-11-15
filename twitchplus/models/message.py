from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from twitchplus import Bot, Channel, Stream, irc

from dataclasses import dataclass


@dataclass
class Message:
    bot: Bot
    nick: str
    channel: str
    content: str
    prefix: str = None
    command: str = None
    args: str = None
    fullargs: str = None

    def get_channel(self) -> Channel:
        return self.bot.get_channel(self.channel)

    def get_stream(self) -> Stream:
        return self.bot.get_stream(self.channel)

    async def reply(self, content: str):
        await self.bot.send(self.channel, content)

    @classmethod
    def from_irc(cls, bot: Bot, irc_msg: irc.Message) -> Message:
        return cls(
            bot,
            nick=irc_msg.nick,
            channel=irc_msg.channel.removeprefix("#"),
            content=irc_msg.content
        )
