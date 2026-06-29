"""
threat_analyzer.py
Recon Rover V1 - Cognitive Layer

Classifies the overall threat level based on spatial, environmental, and health data.
"""

from .world_state import WorldState
from .object_models import CellState

class ThreatAnalyzer:
    """
    Evaluates WorldState to output SAFE, WARNING, or CRITICAL.
    """
    def __init__(self, critical_distance_cm: float = 15.0):
        self.critical_distance = critical_distance_cm

    def evaluate(self, state: WorldState) -> str:
        """
        Calculates threat level. Does not mutate state.
        Returns the calculated level.
        """
        # 1. Check for Critical Threats
        if self._has_critical_obstacle(state):
            return "CRITICAL"
            
        if self._has_critical_hazard(state):
            return "CRITICAL"
            
        if state.battery.is_critical:
            return "CRITICAL"
            
        # 2. Check for Warnings
        if self._has_warning_obstacle(state):
            return "WARNING"
            
        if state.battery.percentage < 20.0:
            return "WARNING"
            
        if state.confidence < 0.5:
            return "WARNING"
            
        # 3. Otherwise Safe
        return "SAFE"

    def _has_critical_obstacle(self, state: WorldState) -> bool:
        """Checks if any obstacle is within critical distance."""
        for cell in state.spatial_grid.values():
            if cell.state == CellState.OBSTACLED and 0 < cell.distance_cm < self.critical_distance:
                return True
        return False
        
    def _has_critical_hazard(self, state: WorldState) -> bool:
        """Checks if any active hazard is critical (e.g. high gas)."""
        for hazard in state.active_hazards:
            if hazard.hazard_type == "gas" and hazard.severity > 0.8:
                return True
        return False
        
    def _has_warning_obstacle(self, state: WorldState) -> bool:
        """Checks if any obstacle is detected at all (which implies it's < obstacle_threshold)."""
        for cell in state.spatial_grid.values():
            if cell.state == CellState.OBSTACLED:
                return True
        return False
