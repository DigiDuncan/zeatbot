import arrow

class Channel:
    __slots__ = [
        "bot", "id", "broadcaster_language", "created_at", "display_name",
        "followers", "game", "language", "logo", "mature", "name", "partner",
        "profile_banner", "profile_banner_background_color", "status",
        "updated_at", "url", "video_banner", "views"
    ]
    def __init__(self, bot):
        self.bot = bot
        self.id = None
        self.broadcaster_language = None
        self.created_at = None
        self.display_name = None
        self.followers = None
        self.game = None
        self.language = None
        self.logo = None
        self.mature = None
        self.name = None
        self.partner = None
        self.profile_banner = None
        self.profile_banner_background_color = None
        self.status = None
        self.updated_at = None
        self.url = None
        self.video_banner = None
        self.views = None

    async def send(self, content):
        await self.bot.send(self.name, content)

    @classmethod
    def from_json(cls, bot, j):
        channel = cls(bot)
        channel.id = int(j["id"])
        channel.broadcaster_language = j["broadcaster_language"]
        channel.created_at = arrow.get(j["created_at"])
        channel.display_name = j["display_name"]
        channel.followers = int(j["followers"])
        channel.game = j["game"]
        channel.language = j["language"]
        channel.logo = j["logo"]
        channel.mature = bool(j["mature"])
        channel.name = j["name"]
        channel.partner = bool(j["partner"])
        channel.profile_banner = j["profile_banner"]
        channel.profile_banner_background_color = j["profile_banner_background_color"]
        channel.status = j["status"]
        channel.updated_at = arrow.get(j["updated_at"])
        channel.url = j["url"]
        channel.video_banner = j["video_banner"]
        channel.views = int(j["views"])
        return channel