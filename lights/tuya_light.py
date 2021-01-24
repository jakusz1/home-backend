import colorsys

from tuyaface.tuyaclient import TuyaClient

from lights.light import Light


class TuyaLight(Light):

    def __init__(self, device_data):
        super().__init__()
        self.device_data = device_data
        self.client = TuyaClient(device_data)
        self.client.start()
        self.update()

    def __del__(self):
        self.client.stop_client()

    def set_rgb_and_brightness(self, r, g, b, br):
        self.client.set_state(self.rgb_brightness_to_tuya_hsv(r, g, b, br), 24)
        self.client.set_state("colour", 21)

        return self.update()

    def set_ct_and_brightness(self, kelvins, br):
        self.client.set_state(br * 10, 22)
        self.client.set_state(self.ct_to_tuya_ct(kelvins), 23)
        self.client.set_state("white", 21)

        return self.update()

    def switch_power(self):
        return self.set_power(not self.power_mode)

    def set_power(self, state):
        self.client.set_state(state, 20)
        return self.update()

    def update(self):
        data = self.client.status()['dps']
        self.power_mode = data['20']
        self.color_mode = data['21'] == 'colour'
        self.red, self.green, self.blue, color_brightness = self.tuya_hsv_to_rgb_brightness(data['24'])
        if self.color_mode:
            self.brightness = color_brightness
        else:
            self.brightness = int(data['22'] / 10)
            self.ct = self.tuya_ct_to_ct(data['23'])
        return self.get_info()

    @staticmethod
    def rgb_brightness_to_tuya_hsv(r, g, b, brightness):
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return f"{int(h * 360):04x}{int(s * 1000):04x}{int(brightness * 10):04x}"

    @staticmethod
    def tuya_hsv_to_rgb_brightness(tuya_hsv):
        h = int(tuya_hsv[:4], 16)
        s = int(tuya_hsv[4:8], 16)
        v = 1.0
        r, g, b = colorsys.hsv_to_rgb(h/360, s/1000, v)
        brightness = int(int(tuya_hsv[8:], 16)/10)
        return int(r*255), int(g*255), int(b*255), brightness

    @staticmethod
    def ct_to_tuya_ct(kelvins):
        return int((kelvins - 1700) / (6500 - 1700) * 1000)

    @staticmethod
    def tuya_ct_to_ct(tuya_ct):
        return int(tuya_ct / 1000 * (6500 - 1700) + 1700)

    def set_all_power(self, state):
        return self.set_power(state)
