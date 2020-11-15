from twitch import TwitchClient


class Client():
    def __init__(self, client_id, oauth_token):
        self._twapi = TwitchClient(client_id, oauth_token)
        self._user_ids = {}

    async def _get_userid(self, name: str) -> int:
        # TODO: Make this async
        if name not in self._user_ids:
            (j,) = self._twapi.users.translate_usernames_to_ids([name])
            self._user_ids[name] = j.id
        return self._user_ids[name]

    async def get_user(self, name: str) -> dict:
        # TODO: Make this async
        userid = await self._get_userid(name)
        j = self._twapi.users.get_by_id(userid)
        return j

    async def get_channel(self, name: str) -> dict:
        # TODO: Make this async
        userid = await self._get_userid(name)
        j = self._twapi.channels.get_by_id(userid)
        return j

    async def get_stream(self, name: str) -> dict:
        # TODO: Make this async
        userid = await self._get_userid(name)
        j = self._twapi.streams.get_stream_by_user(userid)
        return j
