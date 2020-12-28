class Light:
    red = 255
    green = 255
    blue = 255
    brightness = 100
    ct = 4000
    color_mode = True
    power_mode = True
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

    def set_second_rgb_and_brightness(self, r, g, b, br):
        pass

    def switch_second_power(self):
        pass

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
