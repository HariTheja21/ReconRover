"""
Localization Statistics Module
Recon Rover V2 - Phase 3.3
"""
import threading

class LocalizationStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.updates_processed = 0
        
    def increment(self):
        with self._lock:
            self.updates_processed += 1
