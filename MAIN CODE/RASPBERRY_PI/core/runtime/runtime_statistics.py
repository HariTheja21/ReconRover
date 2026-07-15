"""
Runtime Statistics Module
Recon Rover V2 - Phase 3.0
"""
import threading

class RuntimeStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.total_restarts = 0
        self.module_restarts = {}
        
    def increment_restart(self, module_name: str):
        with self._lock:
            self.total_restarts += 1
            if module_name not in self.module_restarts:
                self.module_restarts[module_name] = 0
            self.module_restarts[module_name] += 1
