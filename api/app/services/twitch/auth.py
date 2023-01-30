import requests


class TwitchAuthenticator:
    __base_url = 'https://id.twitch.tv/oauth2/token'

    @classmethod
    def get_access_token(cls, client_id: str, client_secret: str) -> str:
        body = {
            'client_id': client_id,
            'client_secret': client_secret,
            "grant_type": 'client_credentials'
        }

        response = requests.post(cls.__base_url, body)

        return response.json()['access_token']
