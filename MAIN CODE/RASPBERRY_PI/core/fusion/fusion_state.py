"""
Fusion State Module
Recon Rover V2 - Phase 3.2
"""
import threading
import time
from typing import Dict, Any

class FusionState:
    """Holds the raw incoming data before it's correlated and fused."""
    def __init__(self):
        self._lock = threading.RLock()
        self.raw_observations: Dict[str, Dict[str, Any]] = {}
        
    def update_observation(self, sensor_id: str, category: str, value: Any):
        with self._lock:
            if sensor_id not in self.raw_observations:
                self.raw_observations[sensor_id] = {}
            self.raw_observations[sensor_id][category] = {
                "value": value,
                "timestamp": time.time()
            }
            
    def get_all_by_category(self, category: str) -> Dict[str, Any]:
        with self._lock:
            results = {}
            for sid, obs in self.raw_observations.items():
                if category in obs:
                    results[sid] = obs[category]
            return results
