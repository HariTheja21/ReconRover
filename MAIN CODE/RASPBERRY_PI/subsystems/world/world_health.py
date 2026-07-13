"""
world_health.py
Recon Rover V1 - Cognitive Layer

Tracks battery state and propagates confidence into the world model.
"""

from .world_state import WorldState

class WorldHealth:
    def __init__(self, critical_battery_pct: float = 10.0):
        self.critical_battery_pct = critical_battery_pct

    def update(self, state: WorldState, fused_battery: dict, fused_confidence: float) -> bool:
        """
        Updates battery state and confidence.
        Returns True if battery transitions to critical.
        """
        became_critical = False
        
        # Update Battery
        if fused_battery:
            state.battery.percentage = fused_battery.get('percentage', state.battery.percentage)
            state.battery.voltage = fused_battery.get('voltage', state.battery.voltage)
            
            was_critical = state.battery.is_critical
            state.battery.is_critical = state.battery.percentage < self.critical_battery_pct
            
            if state.battery.is_critical and not was_critical:
                became_critical = True
                
        # Propagate Confidence directly from Sensor Fusion for now
        state.confidence = fused_confidence
        
        return became_critical
