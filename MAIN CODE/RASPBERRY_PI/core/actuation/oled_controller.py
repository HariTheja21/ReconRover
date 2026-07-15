"""
OLED Controller Module
Recon Rover V2 - Phase 2.8

Routes display strings.
"""

from typing import Any
from .actuation_events import OLEDCommandRequest

class OLEDController:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        
    def route_command(self, lines: list, clear: bool = True):
        """Publishes the OLED hardware request."""
        # Route to HAL
        req = OLEDCommandRequest(
            lines=lines,
            clear=clear
        )
        self._bus.publish(req)
