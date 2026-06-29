"""
decision_prioritizer.py
Recon Rover V1 - Decision Interpretation & Action Planning

Assigns a numeric execution weight to the action plan.
"""

from .decision_context import DecisionContext

class DecisionPrioritizer:
    def assign_priority(self, requested_priority: str, final_move: str, context: DecisionContext) -> int:
        """
        Returns a score from 0-100.
        """
        score = 50 # Default NORMAL
        
        if requested_priority == "HIGH":
            score = 75
        elif requested_priority == "CRITICAL":
            score = 90
            
        # Safety overrides always bump priority to maximum execution weight
        if final_move == "STOP" and context.hazard_state != "NONE":
            score = 100
            
        if final_move == "STOP" and context.battery_level < 5.0:
            score = 100
            
        return score
