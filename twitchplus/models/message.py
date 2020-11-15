class Message:
    __slots__ = ["bot", "content", "prefix", "channel", "command", "args", "fullargs", "nick"]
    def __init__(self, bot):
        self.bot = bot
        self.content = ""
        self.prefix = None
        self.channel = None
        self.command = None
        self.args = None
        self.fullargs = None
        self.nick = None

    def get_channel(self):
        return self.bot.get_channel(self.channel)

    def get_stream(self):
        return self.bot.get_stream(self.channel)

    async def reply(self, content):
        await self.bot.send(self.channel, content)

    @classmethod
    def from_irc(cls, bot, irc_msg):
        msg = cls(bot)
        msg.nick = irc_msg.nick
        msg.channel = irc_msg.channel.removeprefix("#")
        msg.content = irc_msg.content
        return msg
