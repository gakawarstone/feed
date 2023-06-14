from app.services.http import HttpService


class TwitchAuthenticator:
    __base_url = 'https://id.twitch.tv/oauth2/token'

    @classmethod
    async def get_access_token(cls, client_id: str, client_secret: str) -> str:
        body = {
            'client_id': client_id,
            'client_secret': client_secret,
            "grant_type": 'client_credentials'
        }

        response = await HttpService.post(cls.__base_url, body)
        return response['access_token']
