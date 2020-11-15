from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from twitchplus import Bot

from dataclasses import dataclass

import arrow


@dataclass
class Channel:
    bot: Bot
    id: int
    broadcaster_language: str
    created_at: arrow.Arrow
    display_name: str
    followers: int
    game: str
    language: str
    logo: str
    mature: bool
    name: str
    partner: bool
    profile_banner: str
    profile_banner_background_color: str
    status: str
    updated_at: arrow.Arrow
    url: str
    video_banner: str
    views: int

    async def send(self, content: str):
        await self.bot.send(self.name, content)

    @classmethod
    def from_json(cls, bot: Bot, j: dict) -> Channel:
        return cls(
            bot,
            id = j["id"],
            broadcaster_language = j["broadcaster_language"],
            created_at = arrow.get(j["created_at"]),
            display_name = j["display_name"],
            followers = j["followers"],
            game = j["game"],
            language = j["language"],
            logo = j["logo"],
            mature = j["mature"],
            name = j["name"],
            partner = j["partner"],
            profile_banner = j["profile_banner"],
            profile_banner_background_color = j["profile_banner_background_color"],
            status = j["status"],
            updated_at = arrow.get(j["updated_at"]),
            url = j["url"],
            video_banner = j["video_banner"],
            views = j["views"]
        )
