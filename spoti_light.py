import json
import requests
import time
import toml
import yeelight
import threading
from analyzer import get_color_from_album_url

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class SpotiLight:
    def __init__(self):
        self.config = toml.load("config.toml")
        self.online_bulbs_list = []
        for ip_address, bulb_model in self.config['bulbs']:
            self.online_bulbs_list.append(yeelight.Bulb(ip_address, model=bulb_model))
        self.spotify_thread_running = False
        self.access_token = None
        self.access_token_get_time = None
        self.response = None
        self.thread = None
        self.previously_played_album = {'id': ''}

    def rgb_bulbs(self, func_name, *args):
        fixed_args = [int(arg) for arg in args]
        for bulb in self.online_bulbs_list:
            try:
                light = yeelight.LightType.Main if bulb.model == "color" else yeelight.LightType.Ambient
                getattr(bulb, func_name)(*(fixed_args or []), light_type=light)
            except yeelight.main.BulbException:
                pass

    def white_bulbs(self, func_name, *args):
        for bulb in self.online_bulbs_list:
            try:
                getattr(bulb, func_name)(*(args or []), light_type=yeelight.LightType.Main)
            except yeelight.main.BulbException:
                pass

    def bulb(self, bulb_id, is_main_light, func_name, **kwargs):
        light_type = yeelight.LightType.Main if is_main_light else yeelight.LightType.Ambient
        bulb = self.online_bulbs_list[bulb_id]
        getattr(bulb, func_name)(**(kwargs or {}), light_type=light_type)

    def bulb_info(self, bulb_id):
        return self.online_bulbs_list[bulb_id].get_properties()

    def _spotify(self):
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

        headers = {'authorization': f'Bearer {self.access_token}'}
        currently_playing_request = requests.request(
            "GET", self.config['currently_playing_url'], headers=headers).content
        if currently_playing_request:
            currently_playing = json.loads(currently_playing_request)
            if currently_playing:
                currently_played_album = currently_playing['item']['album']
                if self.previously_played_album['id'] != currently_played_album['id'] and currently_played_album['artists']:
                    print(f"\n{currently_played_album['artists'][0]['name']} - {currently_played_album['name']}")
                    best_rgb = get_color_from_album_url(currently_played_album['images'][-1]['url'])
                    if not best_rgb:
                        best_rgb = self.config['default_color']
                    self.rgb_bulbs("set_rgb", *best_rgb)

                self.previously_played_album = currently_played_album

    def _continous_spotify(self):
        time_counter = 0

        self.rgb_bulbs("turn_on")
        self.rgb_bulbs("set_brightness", 100)

        while True:
            if not self.spotify_thread_running:
                break
            elif time_counter % self.config['time_interval'] == 0:
                self._spotify()

            time.sleep(self.config['tick_time'])
            time_counter += self.config['tick_time']

    def start_spotify(self):
        if not self.spotify_thread_running:
            self.spotify_thread_running = True
            self.thread = threading.Thread(target=self._continous_spotify)
            self.thread.start()
        else:
            raise SpotiLightException("Spotify continous mode is already running")

    def stop_spotify(self):
        if self.spotify_thread_running:
            self.spotify_thread_running = False
            self.thread.join()
        else:
            raise SpotiLightException("Spotify continous mode is not running")

    def single_spotify(self):
        if not self.spotify_thread_running:
            self._spotify()
        else:
            raise SpotiLightException("Spotify continous mode is already running")


class SpotiLightException(Exception):
    pass
