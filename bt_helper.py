import subprocess

HOMEKIT_COMMAND = "python3 -m homekit.put_characteristic -f /home/pi/controller.json -a {} -c {} {}".format
POWER = "1.15"
SATURATION = "1.25"
HUE = "1.24"

class BtHelper:
    @staticmethod
    def set_power(name, status):
        subprocess.Popen(HOMEKIT_COMMAND(name, POWER, status).split())

    @staticmethod
    def set_color(name, saturation, hue):
        subprocess.Popen(f"{HOMEKIT_COMMAND(name, SATURATION, saturation)} -c {HUE} {hue}".split())

    @classmethod
    def set_ct(cls, name, temperature):
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
        cls.set_color(name, saturation, hue)
