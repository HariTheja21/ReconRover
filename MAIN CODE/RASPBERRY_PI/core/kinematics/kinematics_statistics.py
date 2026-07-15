"""
Kinematics Statistics Module
Recon Rover V2 - Phase 4.1
"""
import threading

class KinematicsStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.conversions_performed = 0
        self.saturations_applied = 0
        
    def increment_conversion(self):
        with self._lock:
            self.conversions_performed += 1
            
    def increment_saturation(self):
        with self._lock:
            self.saturations_applied += 1
