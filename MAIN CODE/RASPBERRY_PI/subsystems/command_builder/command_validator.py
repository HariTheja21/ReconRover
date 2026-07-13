"""
command_validator.py
Recon Rover V1 - Command Builder

Validates CommandPackets before they are queued.
"""

from .command_models import CommandPacket, MotorCommand, ServoCommand, LEDCommand, OLEDCommand

class CommandValidator:
    """
    Validates parameter bounds.
    """
    def __init__(self):
        self._validator_ready = True

    def validate(self, packet: CommandPacket) -> bool:
        """
        Returns True if the packet is safe for the hardware.
        """
        if isinstance(packet, MotorCommand):
            mot = packet.mot
            l = mot.get("l", 0.0)
            r = mot.get("r", 0.0)
            if not (-1.0 <= l <= 1.0): return False
            if not (-1.0 <= r <= 1.0): return False

        elif isinstance(packet, ServoCommand):
            srv = packet.srv
            p = srv.get("p", 90.0)
            t = srv.get("t", 90.0)
            if not (0.0 <= p <= 180.0): return False
            if not (0.0 <= t <= 180.0): return False

        elif isinstance(packet, LEDCommand):
            led = packet.led
            r = led.get("r", 0)
            g = led.get("g", 0)
            b = led.get("b", 0)
            if not (0 <= r <= 255): return False
            if not (0 <= g <= 255): return False
            if not (0 <= b <= 255): return False
            if led.get("m", 0) not in [0, 1, 2]: return False

        elif isinstance(packet, OLEDCommand):
            if "anim" not in packet.eye: return False
            anim = packet.eye.get("anim", 0)
            if not isinstance(anim, int): return False
            if not (0 <= anim <= 10): return False

        return True
