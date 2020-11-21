import subprocess
import threading

from enums import DenonKey, DenonInput
from common import singleton
from animations import runRainbow


class PowerStatus:
    def __init__(self):
        self.powered = True

    def switch(self):
        self.powered = not self.powered


@singleton
class IrDenon:
    def __init__(self):
        self.power_status = PowerStatus()
        self.active_input = DenonInput.AMP_CD.lower()
        self.thread = threading.Thread(target=runRainbow, args=(self.power_status,))
        self.thread.start()

    @staticmethod
    def _emit_command(cmd, count):
        subprocess.call(["irsend", "send_once", "denon", cmd, "--count", str(count)])

    def get_info(self):
        return {'power': self.power_status.powered, 'active_input': self.active_input}

    def send(self, command_key, count):
        cmd = getattr(DenonKey, command_key.upper()).value
        if cmd == DenonKey.AMP_POWER:
            self.power_status.switch()
            self._emit_command(cmd, count)
        elif self.power_status.powered:
            try:
                self.active_input = getattr(DenonInput, cmd).lower()
            except AttributeError:
                pass
            self._emit_command(cmd, count)
