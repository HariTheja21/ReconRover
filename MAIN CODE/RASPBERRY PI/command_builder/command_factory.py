"""
command_factory.py
Recon Rover V1 - Command Builder

Translates semantic events into strongly typed CommandPackets.
"""

from event_bus import MovementRequestEvent, EmergencyStopRequested, HazardDetected, BatteryCritical, RecoveryStarted
from .command_models import MotorCommand, LEDCommand, OLEDCommand, CommandPacket
from .command_priority import CommandPriority

class CommandFactory:
    """
    Constructs packets from events.
    """
    def __init__(self):
        pass

    def from_movement_request(self, event: MovementRequestEvent) -> MotorCommand:
        """Maps MovementRequestEvent to MotorCommand."""
        action_map = {
            "MoveForward": "fwd",
            "Reverse": "rev",
            "RotateLeft": "left",
            "RotateRight": "right",
            "Stop": "stop",
            "Wait": "stop"
        }
        
        protocol_action = action_map.get(event.action, "stop")
        # Ensure speed factor (0.0 - 1.0) is converted to 0 - 100
        speed = int(max(0.0, min(1.0, event.speed_factor)) * 100)
        
        return MotorCommand(
            priority=CommandPriority.MOTOR,
            action=protocol_action,
            speed=speed
        )

    def from_emergency_stop(self, event: EmergencyStopRequested) -> MotorCommand:
        return MotorCommand(
            priority=CommandPriority.EMERGENCY,
            action="stop",
            speed=0
        )

    def from_hazard(self, event: HazardDetected) -> LEDCommand:
        return LEDCommand(
            priority=CommandPriority.LED,
            mode="blink",
            r=255, g=0, b=0
        )

    def from_battery_critical(self, event: BatteryCritical) -> OLEDCommand:
        return OLEDCommand(
            priority=CommandPriority.OLED,
            line1="BATTERY CRITICAL",
            line2="System Halting",
            line3="Recharge Imminent",
            line4=""
        )

    def from_recovery(self, event: RecoveryStarted) -> OLEDCommand:
        return OLEDCommand(
            priority=CommandPriority.OLED,
            line1="RECOVERY MODE",
            line2="Attempting escape",
            line3="",
            line4=""
        )
