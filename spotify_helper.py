import json
import http
import time
import threading
import toml
import requests
import yeelight

from analyzer import get_color_from_album_url
from common import singleton


@singleton
class SpotifyHelper:
    def __init__(self):
        self.config = toml.load("config.toml")
        self.access_token = None
        self.access_token_get_time = None
        self.response = None
        self.online_devices = []

    def _get_header(self):
        return {'authorization': f'Bearer {self.access_token}'}

    def _refresh_access_token(self):
        if not self.access_token or \
            time.time() - self.access_token_get_time >= self.response["expires_in"]:
            self.response = json.loads(
                requests.post(
                    self.config['token_url'],
                    data={
                        'grant_type': 'refresh_token',
                        'refresh_token': self.config['refresh_token']
                        },
                    auth=(self.config['client_id'], self.config['client_secret'])).content)
            self.access_token_get_time = time.time()
            self.access_token = self.response["access_token"]

    def get_color_from_currently_played_album(self):
        self._refresh_access_token()

        currently_playing_request = requests.request(
            "GET", self.config['currently_playing_url'], headers=self._get_header()).content

        currently_played_album = json.loads(currently_playing_request)['item']['album']
        best_rgb = get_color_from_album_url(currently_played_album['images'][-1]['url'])
        if not best_rgb:
            best_rgb = self.config['default_color']
        return best_rgb

    def _refresh_devices(self):
        self._refresh_access_token()

        self.online_devices = json.loads(requests.request("GET", f"{self.config['player_url']}/devices", headers=self._get_header()).content)['devices']

    def _get_device_id_by_name(self, name):
        for device in self.online_devices:
            if device['name'] == name:
                return device['id']
        raise SpotiLightException(f"Device {name} is unavailable")

    def _call_player_api(self, method, url, device_name=None, context_uri=None, device_id=None):
        if device_name:
            self._refresh_devices()
            device_id = self._get_device_id_by_name(device_name)
            url = f"{url}?device_id={device_id}"
        elif device_id:
            self._refresh_access_token()
            url = f"{url}?device_id={device_id}"
        else:
            self._refresh_access_token()

        response = requests.request(method, url, json={"context_uri": context_uri} if context_uri else {}, headers=self._get_header())
        return response
    
    def get_currently_playing(self):
        return self._call_player_api("GET", self.config['currently_playing_url'])

    def play(self, device_name=None, context_uri=None, device_id=None):
        return self._call_player_api("PUT", f"{self.config['player_url']}/play", device_name, context_uri, device_id)

    def pause(self, device_name=None):
        return self._call_player_api("PUT", f"{self.config['player_url']}/pause", device_name)

    def next(self, device_name=None):
        return self._call_player_api("POST", f"{self.config['player_url']}/next", device_name)

    def previous(self, device_name=None):
        return self._call_player_api("POST", f"{self.config['player_url']}/previous", device_name)


class SpotiLightException(Exception):
    pass
