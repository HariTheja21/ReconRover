"""
command_dispatcher.py
Recon Rover V1 - Cognitive Layer

Translates high-level intentions into strict ESP32 CommandPackets.
"""

from lifecycle_manager import BaseModule
from event_bus import EventBus, CommandIssued
from config import Config

class CommandDispatcher(BaseModule):
    """
    Provides an API for AI modules to issue commands without knowing JSON.
    """
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self._seq = 0
        
    async def initialize(self):
        self.log.info("CommandDispatcher initialized.")

    async def start(self):
        self.log.info("CommandDispatcher started.")

    async def stop(self):
        self.log.info("CommandDispatcher stopped.")

    def _get_base_payload(self) -> dict:
        self._seq += 1
        return {
            "v_maj": Config.PROTOCOL_VERSION_MAJOR,
            "seq": self._seq
        }

    def set_motor_velocity(self, left: float, right: float):
        """Issue a motor velocity command."""
        payload = self._get_base_payload()
        payload["mot"] = {"l": left, "r": right}
        
        self.event_bus.publish(CommandIssued("MOTOR_VELOCITY", payload))
        self.log.debug(f"Motor velocity command issued: L={left}, R={right}")

    def set_servo_position(self, pan: float, tilt: float):
        """Issue a servo position command."""
        payload = self._get_base_payload()
        payload["srv"] = {"p": pan, "t": tilt}
        
        self.event_bus.publish(CommandIssued("SERVO_POSITION", payload))
        self.log.debug(f"Servo position command issued: Pan={pan}, Tilt={tilt}")

    def set_led_color(self, mode: int, r: int, g: int, b: int):
        """Issue an LED control command."""
        payload = self._get_base_payload()
        payload["led"] = {"m": mode, "r": r, "g": g, "b": b}
        
        self.event_bus.publish(CommandIssued("LED_COLOR", payload))
        self.log.debug(f"LED command issued: Mode={mode}")
