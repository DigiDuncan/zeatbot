import arrow

class User:
    __slots__ = ["bot", "id", "bio", "created_at", "display_name", "logo", "name", "type", "updated_at"]
    def __init__(self, bot):
        self.bot = bot
        self.id = None
        self.bio = None
        self.created_at = None
        self.display_name = None
        self.logo = None
        self.name = None
        self.type = None
        self.updated_at = None

    @classmethod
    def from_json(cls, bot, j):
        user = cls(bot)
        user.id = int(j["id"])
        user.bio = j["bio"]
        user.created_at = arrow.get(j["created_at"])
        user.display_name = j["display_name"]
        user.logo = j["logo"]
        user.name = j["name"]
        user.type = j["type"]
        user.updated_at = arrow.get(j["updated_at"])
        return user
