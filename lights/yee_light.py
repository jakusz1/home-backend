import yeelight

from lights.light import Light


class YeeLight(Light):

    def __init__(self, device_data):
        super().__init__()
        self.device_data = device_data
        self.bulb = yeelight.Bulb(device_data['ip'], model=device_data['model'])
        if self.bulb.model == "ceiling4":
            self.second_light = Light()
        self.update()

    def set_rgb_and_brightness(self, r, g, b, br):
        if self.bulb.model == "color":
            self.bulb.set_rgb(r, g, b, light_type=yeelight.LightType.Main)
            self.bulb.set_brightness(br, light_type=yeelight.LightType.Main)

        return self.update()

    def set_ct_and_brightness(self, kelvins, br):
        self.bulb.set_color_temp(kelvins, light_type=yeelight.LightType.Main)
        self.bulb.set_brightness(br, light_type=yeelight.LightType.Main)

        return self.update()

    def switch_power(self):
        return self.set_power(not self.power_mode)

    def set_power(self, state):
        if state:
            self.bulb.turn_on(light_type=yeelight.LightType.Main)
        else:
            self.bulb.turn_off(light_type=yeelight.LightType.Main)
        return self.update()

    def update(self):
        data = self.bulb.get_properties()
        self.power_mode = data['power'] == 'on'
        self.brightness = int(data['bright'])
        self.red, self.green, self.blue = self.rgb_integer_to_rgb(int(data['rgb'] or 0))
        self.ct = int(data['ct'])
        self.color_mode = data['color_mode'] == '1'

        if self.second_light:
            self.second_light.power_mode = data['bg_power'] == 'on'
            self.brightness = int(data['bg_bright'])
            self.second_light.red, self.second_light.green, self.second_light.blue = self.rgb_integer_to_rgb(
                int(data['bg_rgb']))
        return self.get_info()

    @staticmethod
    def rgb_integer_to_rgb(rgb_int):
        return (rgb_int >> 16) & 255, (rgb_int >> 8) & 255, rgb_int & 255

    def set_second_rgb_and_brightness(self, r, g, b, br):
        if self.second_light:
            self.bulb.set_rgb(r, g, b, light_type=yeelight.LightType.Ambient)
            self.bulb.set_brightness(br, light_type=yeelight.LightType.Ambient)

        return self.update()

    def switch_second_power(self):
        return self.set_second_power(not self.second_light.power_mode)

    def set_second_power(self, state):
        if self.second_light:
            if state:
                self.bulb.turn_on(light_type=yeelight.LightType.Ambient)
            else:
                self.bulb.turn_off(light_type=yeelight.LightType.Ambient)
        return self.update()
