"""
Hardware Bridge Statistics Module
Recon Rover V2 - Phase 4.2
"""
import threading

class HardwareBridgeStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.packets_encoded = 0
        self.invalid_requests = 0
        
    def increment_encoded(self):
        with self._lock:
            self.packets_encoded += 1
            
    def increment_invalid(self):
        with self._lock:
            self.invalid_requests += 1
