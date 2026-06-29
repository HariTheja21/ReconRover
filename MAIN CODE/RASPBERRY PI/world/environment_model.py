"""
environment_model.py
Recon Rover V1 - Cognitive Layer

Tracks persistent environmental state (e.g., gas hazards).
"""

from typing import List
from .object_models import Hazard
from .world_state import WorldState

class EnvironmentModel:
    def __init__(self):
        # We could track historical hazards, but for now we just 
        # keep the WorldState active_hazards updated.
        pass
        
    def update(self, state: WorldState, gas_detected: bool, gas_confidence: float, timestamp_ms: int) -> bool:
        """
        Updates the environmental hazards in the world state.
        Returns True if a new hazard was added or cleared (state change).
        """
        changed = False
        
        # Check if gas hazard already exists in state
        gas_hazard = next((h for h in state.active_hazards if h.hazard_type == "gas"), None)
        
        if gas_detected:
            if not gas_hazard:
                # New hazard appeared
                new_hazard = Hazard(
                    hazard_type="gas", 
                    severity=1.0, 
                    confidence=gas_confidence, 
                    timestamp_ms=timestamp_ms
                )
                state.active_hazards.append(new_hazard)
                changed = True
            else:
                # Update existing hazard
                gas_hazard.confidence = gas_confidence
                gas_hazard.timestamp_ms = timestamp_ms
        else:
            if gas_hazard:
                # Hazard cleared
                state.active_hazards.remove(gas_hazard)
                changed = True
                
        return changed
