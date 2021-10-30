import requests
import toml


class Projector:
    API_URL = toml.load("config.toml")['esp32_api_url']

    @classmethod
    def update(cls):
        resp = requests.post(cls.API_URL)
        return resp.json()

    @classmethod
    def switch_power(cls):
        resp = requests.get(cls.API_URL)
        return resp.json()
