import toml
import yeelight

from analyzer import get_color_from_album_url
from common import singleton


@singleton
class LightHelper:
    def __init__(self):
        self.config = toml.load("config.toml")
        self.online_bulbs_list = []
        for ip_address, bulb_model in self.config['bulbs']:
            self.online_bulbs_list.append(yeelight.Bulb(ip_address, model=bulb_model))

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
        try:
            getattr(bulb, func_name)(**(kwargs or {}), light_type=light_type)
        except yeelight.main.BulbException:
            pass

    def bulb_info(self, bulb_id):
        return self.online_bulbs_list[bulb_id].get_properties()

