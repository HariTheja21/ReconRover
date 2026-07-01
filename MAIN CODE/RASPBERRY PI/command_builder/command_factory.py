"""
command_factory.py
Recon Rover V1 - Command Builder

Translates semantic events into strongly typed CommandPackets.
"""

from event_bus import MovementRequestEvent, EmergencyStopRequested, HazardDetected, BatteryCritical, RecoveryStarted
from .command_models import MotorCommand, LEDCommand, OLEDCommand, CommandPacket
from .command_priority import CommandPriority
from typing import Dict

class CommandFactory:
    """
    Constructs packets from events.
    """
    def __init__(self):
        pass

    def from_motor_speeds(self, speeds: Dict[str, float], priority: CommandPriority = CommandPriority.MOTOR) -> MotorCommand:
        """Maps a left/right speed dict (from MotionPlanner) to a MotorCommand."""
        return MotorCommand(
            priority=priority,
            mot={"l": speeds.get("l", 0.0), "r": speeds.get("r", 0.0)}
        )

    def from_hazard(self, event: HazardDetected) -> LEDCommand:
        """Maps hazard event to flashing red LED."""
        return LEDCommand(
            priority=CommandPriority.LED,
            led={"m": 1, "r": 255, "g": 0, "b": 0} # mode 1 = blink
        )

    def from_battery_critical(self, event: BatteryCritical) -> OLEDCommand:
        """Maps battery critical to the appropriate eye animation."""
        return OLEDCommand(
            priority=CommandPriority.OLED,
            eye={"anim": 2} # 2 = battery critical anim
        )

    def from_recovery(self, event: RecoveryStarted) -> OLEDCommand:
        """Maps recovery to the appropriate eye animation."""
        return OLEDCommand(
            priority=CommandPriority.OLED,
            eye={"anim": 3} # 3 = recovery anim
        )
