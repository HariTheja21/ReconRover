"""
Serial Health Module
Recon Rover V2 - Phase 2.4

Publishes low-level health reports about the physical Serial layer.
"""

import time
from typing import Any
from .serial_statistics import SerialStatistics
from .hal_events import SerialHealthUpdated

class SerialHealth:
    """
    Periodically checks the statistics and broadcasts SerialHealthUpdated.
    """
    
    def __init__(self, event_bus: Any, stats: SerialStatistics):
        self._bus = event_bus
        self._stats = stats
        self._start_time = time.time()
        self.is_connected = False
        
    def set_connected_state(self, state: bool):
        self.is_connected = state
        
    def broadcast_health(self):
        """
        Publishes the current health snapshot to the EventBus.
        """
        snapshot = self._stats.get_snapshot()
        uptime_ms = int((time.time() - self._start_time) * 1000)
        
        event = SerialHealthUpdated(
            is_connected=self.is_connected,
            bytes_rx=snapshot["bytes_rx"],
            bytes_tx=snapshot["bytes_tx"],
            crc_errors=snapshot["crc_errors"],
            dropped_packets=snapshot["dropped_packets"],
            uptime_ms=uptime_ms
        )
        self._bus.publish(event)
