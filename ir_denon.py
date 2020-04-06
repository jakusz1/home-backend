import subprocess

from keys import DenonKey

class IrDenon:
    @staticmethod
    def send(command_key, count=2):
        cmd = getattr(DenonKey, command_key.upper())
        subprocess.call(["irsend", "send_once", "denon", str(cmd), "--count", int(count)])
