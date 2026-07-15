"""
Fusion Rules Module
Recon Rover V2 - Phase 3.2
"""
import time

class FusionRules:
    """Stateless rules engine for combining conflicting data points."""
    
    @staticmethod
    def fuse_distance(observations: dict, confidences: dict) -> tuple:
        """
        Takes {sensor_id: {"value": distance, "timestamp": t}}
        Returns (fused_distance, fused_confidence, contributing_sensors)
        Prioritizes lowest distance for safety, weighted by confidence.
        """
        if not observations:
            return None, 0.0, []
            
        now = time.time()
        valid = {}
        for sid, obs in observations.items():
            if now - obs["timestamp"] < 1.0: # 1 sec TTL
                valid[sid] = obs
                
        if not valid:
            return None, 0.0, []
            
        # For distances, the safest fusion is often picking the closest object,
        # but we filter out ultra-low confidence ghosts.
        best_dist = float('inf')
        total_conf = 0.0
        sensors_used = []
        
        for sid, obs in valid.items():
            c = confidences.get(sid, 0.5)
            if c > 0.3: # Minimum confidence threshold
                if obs["value"] < best_dist:
                    best_dist = obs["value"]
                total_conf += c
                sensors_used.append(sid)
                
        if not sensors_used:
            return None, 0.0, []
            
        avg_conf = total_conf / len(sensors_used)
        return best_dist, avg_conf, sensors_used
