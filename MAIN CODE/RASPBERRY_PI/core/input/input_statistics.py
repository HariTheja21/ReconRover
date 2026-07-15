"""
Input Statistics Module
Recon Rover V2 - Phase 2.6

Thread-safe tracking for physical input metrics.
"""

import threading

class InputStatistics:
    """Maintains counts of raw inputs and generated intents."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self.raw_events_rx = 0
        self.events_dropped_deadzone = 0
        self.intents_generated = 0
        
    def add_rx(self):
        with self._lock:
            self.raw_events_rx += 1
            
    def add_dropped(self):
        with self._lock:
            self.events_dropped_deadzone += 1
            
    def add_intent(self):
        with self._lock:
            self.intents_generated += 1
            
    def get_snapshot(self) -> dict:
        with self._lock:
            return {
                "raw_events_rx": self.raw_events_rx,
                "events_dropped_deadzone": self.events_dropped_deadzone,
                "intents_generated": self.intents_generated
            }
