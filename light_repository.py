import json

import toml
from multiprocessing import Process

from common import singleton
from lights.tuya_light import TuyaLight
from lights.yee_light import YeeLight


@singleton
class LightRepository:
    def __init__(self):
        self.config = toml.load("config.toml")
        self.lights = {}
        for light in self.config['light']:
            if light['type'] == 'yee':
                self.lights[light['name']] = YeeLight(light['device_data'])
            elif light['type'] == 'tuya':
                self.lights[light['name']] = TuyaLight(light['device_data'])

    def get_light_by_name(self, name):
        return self.lights[name]

    def get_info(self):
        return {k: v.get_info() for k, v in self.lights.items()}

    def set_all_power(self, state):
        # proc = []
        # for light in self.lights.values():
        #     if light.power_mode != state:
        #         p = Process(target=light.set_all_power, args=(state,))
        #         p.start()
        #         proc.append(p)
        # for p in proc:
        #     p.join()
        for light in self.lights.values():
            if light.power_mode != state:
                light.set_power(state)
                light.set_second_power(state)
        return self.get_info()
