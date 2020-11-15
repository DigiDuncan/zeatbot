from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from twitchplus import Bot

from dataclasses import dataclass

import arrow


@dataclass
class Stream:
    bot: Bot
    id: int
    game: str
    viewers: int
    video_height: int
    average_fps: int
    delay: int
    created_at: arrow.Arrow
    is_playlist: bool
    preview_small: str
    preview_medium: str
    preview_large: str
    preview_template: str

    @classmethod
    def from_json(cls, bot: Bot, j: dict) -> Stream:
        if j is None:
            return None
        return cls(
            bot,
            id = j["id"],
            game = j["game"],
            viewers = j["viewers"],
            video_height = j["video_height"],
            average_fps = j["average_fps"],
            delay = j["delay"],
            created_at = arrow.get(j["created_at"]),
            is_playlist = j["is_playlist"],
            preview_small = j["preview"]["small"],
            preview_medium = j["preview"]["medium"],
            preview_large = j["preview"]["large"],
            preview_template = j["preview"]["template"]
        )
