"""
Hardware Statistics Module
Recon Rover V2 - Phase 2.8

Thread-safe telemetry tracking for actuation requests.
"""

import threading
import time

class HardwareStatistics:
    """Tracks commands routed per second."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self.total_commands_routed = 0
        self.commands_per_second = 0.0
        
        self._last_calc_time = time.time()
        self._commands_since_last_calc = 0
        
    def add_command(self):
        with self._lock:
            self.total_commands_routed += 1
            self._commands_since_last_calc += 1
            self._recalc_hz()
            
    def _recalc_hz(self):
        now = time.time()
        dt = now - self._last_calc_time
        if dt >= 1.0:
            self.commands_per_second = self._commands_since_last_calc / dt
            self._commands_since_last_calc = 0
            self._last_calc_time = now

    def get_snapshot(self) -> dict:
        with self._lock:
            self._recalc_hz()
            return {
                "total_commands_routed": self.total_commands_routed,
                "commands_per_second": round(self.commands_per_second, 2)
            }
