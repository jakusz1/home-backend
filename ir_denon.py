import json
import subprocess

from enums import DenonKey, DenonInput
from common import singleton

@singleton
class IrDenon:
    def __init__(self):
        self.power_status = True
        self.active_input = DenonInput.AMP_CD

    def to_json(self):
        return json.dumps(self.__dict__)

    def send(self, command_key, count):
        cmd = getattr(DenonKey, command_key.upper()).value
        if cmd == DenonKey.AMP_POWER:
            self.power_status = not self.power_status
        else:
            try:
                self.active_input = getattr(DenonInput, cmd)
            except AttributeError:
                pass
        subprocess.call(["irsend", "send_once", "denon", cmd, "--count", str(count)])
