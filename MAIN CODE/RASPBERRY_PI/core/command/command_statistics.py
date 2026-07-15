"""
Command Statistics Module
Recon Rover V2 - Phase 2.5

Thread-safe counters for the command pipeline throughput.
"""

import threading

class CommandStatistics:
    """Maintains exact counts of command state transitions."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self.processed = 0
        self.rejected = 0
        self.sent = 0
        
    def add_processed(self):
        with self._lock:
            self.processed += 1
            
    def add_rejected(self):
        with self._lock:
            self.rejected += 1
            
    def add_sent(self):
        with self._lock:
            self.sent += 1
            
    def get_snapshot(self) -> dict:
        with self._lock:
            return {
                "processed": self.processed,
                "rejected": self.rejected,
                "sent": self.sent
            }
