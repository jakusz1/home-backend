class Light:
    red = 255
    green = 255
    blue = 255
    brightness = 100
    ct = 4000
    color_mode = True
    power_mode = False
    second_light = None

    def __init__(self):
        pass

    def set_rgb_and_brightness(self, r, g, b, br):
        pass

    def set_ct_and_brightness(self, kelvins, br):
        pass

    def switch_power(self):
        pass

    def set_power(self, state):
        pass

    def update(self):
        pass

    def set_second_power(self, state):
        pass

    def set_all_power(self, state):
        pass

    def set_second_rgb_and_brightness(self, r, g, b, br):
        pass

    def switch_second_power(self):
        pass

    def set_scene(self, scene):
        self.set_power(scene.get("power_mode"))
        if scene.get("power_mode"):
            if scene.get("color_mode"):
                self.set_rgb_and_brightness(scene.get("red"),
                                            scene.get("green"),
                                            scene.get("blue"),
                                            scene.get("brightness"))
            else:
                self.set_ct_and_brightness(scene.get("ct"), scene.get("brightness"))
        if self.second_light:
            second_light_data = scene.get("second_light")
            self.set_second_power(second_light_data.get("power_mode"))
            if second_light_data.get("power_mode"):
                self.set_second_rgb_and_brightness(second_light_data.get("red"),
                                                   second_light_data.get("green"),
                                                   second_light_data.get("blue"),
                                                   second_light_data.get("brightness"))

    def get_info(self):
        return {
            'red': self.red,
            'green': self.green,
            'blue': self.blue,
            'brightness': self.brightness,
            'ct': self.ct,
            'color_mode': self.color_mode,
            'power_mode': self.power_mode,
            'second_light': self.second_light.get_info() if self.second_light else None
        }

    def update_info(self, json):
        self.red = json['red']
        self.green = json['green']
        self.blue = json['blue']
        self.brightness = json['brightness']
        self.ct = json['ct']
        self.color_mode = json['color_mode']
        self.power_mode = json['power_mode']
        if self.second_light:
            self.second_light.update_info(json['second_light'])
