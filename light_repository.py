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
        proc = []
        for light in self.lights.values():
            if light.power_mode != state:
                if isinstance(light, YeeLight):
                    p = Process(target=light.set_all_power, args=(state,))
                    p.start()
                    proc.append(p)
                else:
                    light.set_power(state)
        for p in proc:
            p.join()
        for light in self.lights.values():
            if light.power_mode != state:
                if isinstance(light, YeeLight):
                    light.update()
        return self.get_info()

    def set_scene(self, scene_name):
        scene = toml.load(f"scenes/{scene_name}.toml")
        for light_name, light in self.lights.items():
            light_data = scene.get(light_name)
            light.set_power(light_data.get("power_mode"))
            if light_data.get("power_mode"):
                if light_data.get("color_mode"):
                    light.set_rgb_and_brightness(light_data.get("red"),
                                                 light_data.get("green"),
                                                 light_data.get("blue"),
                                                 light_data.get("brightness"))
                else:
                    light.set_ct_and_brightness(light_data.get("ct"), light_data.get("brightness"))
            if light.second_light:
                second_light_data = light_data.get("second_light")
                light.second_light.set_second_power(second_light_data.get("power_mode"))
                if second_light_data.get("power_mode"):
                    light.second_light.set_second_rgb_and_brightness(second_light_data.get("red"),
                                                                     second_light_data.get("green"),
                                                                     second_light_data.get("blue"),
                                                                     second_light_data.get("brightness"))
