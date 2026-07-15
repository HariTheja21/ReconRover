"""
Motor Controller Module
Recon Rover V2 - Phase 2.8

Constrains motor PWM requests based on Configuration values (limits, polarity).
"""

from typing import Any, Tuple
from .actuation_events import MotorCommandRequest

class MotorController:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        
        # Safe defaults
        self.max_pwm = 255
        self.invert_left = False
        self.invert_right = False
        
    def update_config(self, config: dict):
        """Updates internal constraints based on the global configuration."""
        self.max_pwm = config.get("motors", {}).get("max_pwm", 255)
        self.invert_left = config.get("motors", {}).get("invert_left", False)
        self.invert_right = config.get("motors", {}).get("invert_right", False)
        
    def route_command(self, left_pwm: int, right_pwm: int, duration_ms: int):
        """Validates, constrains, and publishes the motor hardware request."""
        
        # Clamp
        left = max(-self.max_pwm, min(self.max_pwm, left_pwm))
        right = max(-self.max_pwm, min(self.max_pwm, right_pwm))
        
        # Invert if configured
        if self.invert_left:
            left = -left
        if self.invert_right:
            right = -right
            
        # Ensure duration is valid
        dur = max(0, duration_ms)
        
        # Route to HAL
        req = MotorCommandRequest(
            left_pwm=left,
            right_pwm=right,
            duration_ms=dur
        )
        self._bus.publish(req)
