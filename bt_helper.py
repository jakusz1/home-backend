import subprocess

from homekit.controller import Controller
from common import singleton

POWER = "1.15"
SATURATION = "1.25"
HUE = "1.24"

@singleton
class BtHelper:
    def __init__(self):
        self.controller = Controller('hci0')
        self.controller.load_data('/home/pi/controller.json')

    def _set(self, alias, charac):
        pairing = self.controller.get_pairings()[alias]

        characteristics = [(int(c[0].split('.')[0]),  # the first part is the aid, must be int
                            int(c[0].split('.')[1]),  # the second part is the iid, must be int
                            c[1]) for c in charac]
        results = pairing.put_characteristics(characteristics, do_conversion=True)

    def set_power(self, name, status):
        self._set(name, [(POWER, status)])

    def set_color(self, name, saturation, hue):
        self._set(name, [(SATURATION, saturation), (HUE, hue)])

    def set_ct(self, name, temperature):
        if temperature >= 6000:
            saturation = 0
            hue = 180
        elif temperature >= 4800:
            saturation = 0
            hue = 300
        elif temperature >= 3000:
            saturation = 0
            hue = 0
        elif temperature >= 2200:
            saturation = 55
            hue = 30
        else:
            saturation = 100
            hue = 25
        self.set_color(name, saturation, hue)
