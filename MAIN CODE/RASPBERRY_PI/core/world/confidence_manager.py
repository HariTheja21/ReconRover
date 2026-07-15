"""
Confidence Manager Module
Recon Rover V2 - Phase 3.1
"""
import threading
import time

class ConfidenceManager:
    """Decays confidence of sensory observations over time."""
    def __init__(self):
        self._lock = threading.RLock()
        
    def decay_confidence(self, initial_confidence: float, timestamp: float, decay_rate: float = 0.1) -> float:
        """Linear decay based on time elapsed."""
        elapsed = time.time() - timestamp
        new_conf = initial_confidence - (elapsed * decay_rate)
        return max(0.0, min(1.0, new_conf))
