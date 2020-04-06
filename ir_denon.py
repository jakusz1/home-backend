import subprocess

from keys import DenonKey

class IrDenon:
    @staticmethod
    def send(command_key, count):
        cmd = getattr(DenonKey, command_key.upper())
        subprocess.call(["irsend", "send_once", "denon", str(cmd), "--count", count])
