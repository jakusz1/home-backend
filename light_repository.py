import multiprocessing
from logger import logger

import toml

from common import singleton
from lights.tuya_light import TuyaLight
from lights.yee_light import YeeLight
from process import Process


@singleton
class LightRepository:
    def __init__(self):
        self.config = toml.load("config.toml")
        self.lights = {}
        for light in self.config['light']:
            try:
                if light['type'] == 'yee':
                    self.lights[light['name']] = YeeLight(light['device_data'])
                elif light['type'] == 'tuya':
                    self.lights[light['name']] = TuyaLight(light['device_data'])
            except Exception as error:
                logger.warning(f"{light['name']} not connected: {error}")
        self.return_dict = multiprocessing.Manager().dict()

    def get_light_by_name(self, name):
        return self.lights.get(name, None)

    def get_info(self):
        return {k: v.get_info() for k, v in self.lights.items()}

    def set_power(self, state):
        proc = []
        for light_name, light in self.lights.items():
            if isinstance(light, YeeLight):
                p = Process(target=light.set_all_power_with_retry, args=(state, light_name, self.return_dict))
                p.start()
                proc.append(p)
        for light in self.lights.values():
            if light.power_mode != state:
                if isinstance(light, TuyaLight):
                    light.set_power(state)
        for p in proc:
            p.join()
        for light_name, light in self.lights.items():
            if isinstance(light, YeeLight):
                light.update_info(self.return_dict[light_name])
        return self.get_info()

    def set_scene(self, scene_name):
        scene = toml.load(f"scenes/{scene_name}.toml")
        proc = []
        for light_name, light in self.lights.items():
            if isinstance(light, YeeLight):
                p = Process(target=light.set_scene_with_retry, args=(scene.get(light_name), light_name, self.return_dict))
                p.start()
                proc.append(p)
        for light_name, light in self.lights.items():
            if isinstance(light, TuyaLight):
                light.set_scene(scene.get(light_name))
        for p in proc:
            p.join()
        for light_name, light in self.lights.items():
            if isinstance(light, YeeLight):
                light.update_info(self.return_dict[light_name])
        return self.get_info()
