"""
command_validator.py
Recon Rover V1 - Command Builder

Validates CommandPackets before they are queued.
"""

from .command_models import CommandPacket, MotorCommand, ServoCommand, LEDCommand

class CommandValidator:
    """
    Validates parameter bounds.
    """
    def __init__(self):
        pass

    def validate(self, packet: CommandPacket) -> bool:
        """
        Returns True if the packet is safe for the hardware.
        """
        if isinstance(packet, MotorCommand):
            if not (0 <= packet.speed <= 100):
                return False
            if packet.action not in ["fwd", "rev", "left", "right", "stop"]:
                return False

        elif isinstance(packet, ServoCommand):
            if not (0 <= packet.pan_angle <= 180):
                return False
            if not (0 <= packet.tilt_angle <= 180):
                return False

        elif isinstance(packet, LEDCommand):
            if not (0 <= packet.r <= 255): return False
            if not (0 <= packet.g <= 255): return False
            if not (0 <= packet.b <= 255): return False
            if packet.mode not in ["solid", "blink", "pulse"]: return False

        return True
