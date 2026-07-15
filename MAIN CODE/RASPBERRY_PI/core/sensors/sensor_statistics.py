"""
Sensor Statistics Module
Recon Rover V2 - Phase 2.9

Thread-safe telemetry tracking for inbound sensor packets.
"""

import threading
import time

class SensorStatistics:
    """Tracks packets decoded per second."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self.total_packets_decoded = 0
        self.packets_per_second = 0.0
        
        self._last_calc_time = time.time()
        self._packets_since_last_calc = 0
        
    def add_packet(self):
        with self._lock:
            self.total_packets_decoded += 1
            self._packets_since_last_calc += 1
            self._recalc_hz()
            
    def _recalc_hz(self):
        now = time.time()
        dt = now - self._last_calc_time
        if dt >= 1.0:
            self.packets_per_second = self._packets_since_last_calc / dt
            self._packets_since_last_calc = 0
            self._last_calc_time = now

    def get_snapshot(self) -> dict:
        with self._lock:
            self._recalc_hz()
            return {
                "total_packets_decoded": self.total_packets_decoded,
                "packets_per_second": round(self.packets_per_second, 2)
            }
