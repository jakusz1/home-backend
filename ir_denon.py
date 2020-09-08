import json
import subprocess
import threading

from enums import DenonKey, DenonInput
from common import singleton
from animations import runRainbow

@singleton
class IrDenon:
    def __init__(self):
        self.power_status = True
        self.active_input = DenonInput.AMP_CD
        self.thread = threading.Thread(target=runRainbow, args=(self.power_status,))

    @staticmethod
    def _emit_command(cmd, count):
        subprocess.call(["irsend", "send_once", "denon", cmd, "--count", str(count)])

    def to_json(self):
        return json.dumps({'power_status': self.power_status, 'active_input': self.active_input})

    def send(self, command_key, count):
        cmd = getattr(DenonKey, command_key.upper()).value
        if cmd == DenonKey.AMP_POWER:
            self.power_status = not self.power_status
            self._emit_command(cmd, count)
        elif self.power_status:
            try:
                self.active_input = getattr(DenonInput, cmd)
            except AttributeError:
                pass
            self._emit_command(cmd, count)
