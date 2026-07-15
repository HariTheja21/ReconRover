"""
Fusion Engine Module
Recon Rover V2 - Phase 3.2
"""
import threading
from .fusion_state import FusionState
from .fusion_rules import FusionRules
from .sensor_correlator import SensorCorrelator
from .sensor_confidence import SensorConfidence

class FusionEngine:
    """Core processor that correlates state and applies rules."""
    def __init__(self):
        self.state = FusionState()
        self.confidence = SensorConfidence()
        
    def process_category(self, category: str) -> tuple:
        """
        Returns (fused_value, fused_confidence, contributing_sensors, penalized_sensors)
        """
        observations = self.state.get_all_by_category(category)
        
        # 1. Detect conflicts
        outliers = SensorCorrelator.detect_conflicts(category, observations)
        for sid in outliers:
            self.confidence.apply_decay(sid, 0.1) # Penalize contradictory sensors
            
        # 2. Extract current confidences
        conf_map = {sid: self.confidence.get_confidence(sid) for sid in observations.keys()}
        
        # 3. Apply fusion rules
        if category == "distance":
            val, conf, sensors = FusionRules.fuse_distance(observations, conf_map)
            return val, conf, sensors, outliers
            
        return None, 0.0, [], []
