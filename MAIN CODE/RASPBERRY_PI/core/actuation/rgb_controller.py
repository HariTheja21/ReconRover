"""
RGB Controller Module
Recon Rover V2 - Phase 2.8

Constrains RGB requests.
"""

from typing import Any
from .actuation_events import RGBCommandRequest

class RGBController:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.max_brightness = 100
        
    def update_config(self, config: dict):
        """Updates internal constraints based on the global configuration."""
        self.max_brightness = config.get("rgb", {}).get("max_brightness", 100)
        
    def route_command(self, red: int, green: int, blue: int, brightness: int = 100):
        """Validates, constrains, and publishes the RGB hardware request."""
        
        # Clamp colors to 0-255
        r = max(0, min(255, red))
        g = max(0, min(255, green))
        b = max(0, min(255, blue))
        
        # Clamp brightness
        bright = max(0, min(self.max_brightness, brightness))
        
        # Route to HAL
        req = RGBCommandRequest(
            red=r,
            green=g,
            blue=b,
            brightness=bright
        )
        self._bus.publish(req)
