"""
Buzzer Controller Module
Recon Rover V2 - Phase 2.8

Routes buzzer requests.
"""

from typing import Any
from .actuation_events import BuzzerCommandRequest

class BuzzerController:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        
    def route_command(self, frequency_hz: int, duration_ms: int):
        """Publishes the buzzer hardware request."""
        # Route to HAL
        req = BuzzerCommandRequest(
            frequency_hz=frequency_hz,
            duration_ms=duration_ms
        )
        self._bus.publish(req)
