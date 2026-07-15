"""
Servo Controller Module
Recon Rover V2 - Phase 2.8

Constrains servo angle requests based on Configuration values (limits).
"""

from typing import Any
from .actuation_events import ServoCommandRequest

class ServoController:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.limits = {} # mapping servo_id -> (min, max)
        
    def update_config(self, config: dict):
        """Updates internal constraints based on the global configuration."""
        self.limits = config.get("servos", {})
        
    def route_command(self, servo_id: int, angle: int):
        """Validates, constrains, and publishes the servo hardware request."""
        
        # Apply limits if configured for this ID, else assume standard 0-180
        min_ang, max_ang = self.limits.get(str(servo_id), (0, 180))
        
        # Clamp
        safe_angle = max(min_ang, min(max_ang, angle))
        
        # Route to HAL
        req = ServoCommandRequest(
            servo_id=servo_id,
            angle=safe_angle
        )
        self._bus.publish(req)
