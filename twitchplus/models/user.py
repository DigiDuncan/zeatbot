from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from twitchplus import Bot

from dataclasses import dataclass

import arrow


@dataclass
class User:
    bot: Bot
    id: int
    bio: str
    created_at: arrow.Arrow
    display_name: str
    logo: str
    name: str
    type: str
    updated_at: arrow.Arrow

    @classmethod
    def from_json(cls, bot: Bot, j: dict) -> User:
        return cls(
            bot,
            id = int(j["id"]),
            bio = j["bio"],
            created_at = arrow.get(j["created_at"]),
            display_name = j["display_name"],
            logo = j["logo"],
            name = j["name"],
            type = j["type"],
            updated_at = arrow.get(j["updated_at"])
        )
