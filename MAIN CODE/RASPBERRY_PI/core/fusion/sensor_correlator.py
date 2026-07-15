"""
Sensor Correlator Module
Recon Rover V2 - Phase 3.2
"""
from typing import Tuple, Dict, Any
import time

class SensorCorrelator:
    """Identifies contradictory information between sensors."""
    
    @staticmethod
    def detect_conflicts(category: str, observations: Dict[str, Any]) -> list:
        """Returns a list of sensor_ids that wildly disagree with the consensus."""
        if not observations or len(observations) < 2:
            return []
            
        now = time.time()
        valid_vals = [obs["value"] for obs in observations.values() if now - obs["timestamp"] < 1.0]
        
        if len(valid_vals) < 2:
            return []
            
        # Simple median outlier detection
        sorted_vals = sorted(valid_vals)
        median = sorted_vals[len(sorted_vals)//2]
        
        outliers = []
        for sid, obs in observations.items():
            if now - obs["timestamp"] < 1.0:
                val = obs["value"]
                # If a sensor differs from median by more than 50%
                if abs(val - median) > (median * 0.5 + 5.0): 
                    outliers.append(sid)
                    
        return outliers
