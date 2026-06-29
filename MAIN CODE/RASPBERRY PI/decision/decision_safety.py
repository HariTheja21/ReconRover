"""
decision_safety.py
Recon Rover V1 - Decision Interpretation & Action Planning

The ultimate veto authority. Overrides AI intents based on hard safety constraints.
"""

from .decision_context import DecisionContext

class DecisionSafety:
    def check_safety_override(self, requested_move: str, context: DecisionContext) -> str:
        """
        Returns the requested move if safe, or 'STOP' if a safety constraint is violated.
        """
        
        # 1. Hazard Veto
        if context.hazard_state != "NONE":
            return "STOP"
            
        # 2. Battery Veto
        if context.battery_level < 5.0: # 5% is critical cutoff
            return "STOP"
            
        # 3. Health Veto
        if context.health_status == "CRITICAL":
            return "STOP"
            
        # 4. Safe to proceed
        return requested_move
