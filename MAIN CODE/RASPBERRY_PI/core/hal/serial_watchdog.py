"""
Serial Watchdog Module
Recon Rover V2 - Phase 2.4

Detects communication hangs at the physical layer and broadcasts timeouts.
"""

import time
from typing import Any
from .hal_events import CommunicationTimeout

class SerialWatchdog:
    """
    Monitors the time since the last valid packet was received from the Serial port.
    """
    
    def __init__(self, event_bus: Any, timeout_ms: int = 5000):
        self._bus = event_bus
        self.timeout_ms = timeout_ms
        self._last_seen_ms = int(time.time() * 1000)
        self._timeout_triggered = False
        
    def ping(self):
        """Called whenever a valid packet is received to reset the watchdog."""
        self._last_seen_ms = int(time.time() * 1000)
        self._timeout_triggered = False
        
    def check(self) -> bool:
        """
        Evaluates the watchdog condition.
        Returns True if a timeout just occurred.
        """
        now = int(time.time() * 1000)
        delta = now - self._last_seen_ms
        
        if delta > self.timeout_ms and not self._timeout_triggered:
            self._timeout_triggered = True
            self._bus.publish(CommunicationTimeout(
                threshold_ms=self.timeout_ms,
                last_seen_ms=self._last_seen_ms
            ))
            return True
        return False
