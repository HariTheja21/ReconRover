"""
ai_rules.py
Recon Rover V1 - AI Decision Engine

Deterministic rule engine defining state transition logic.
"""

from .ai_context import AIContext
from .ai_state_machine import AIState

class AIRuleEngine:
    def __init__(self):
        pass

    def evaluate(self, context: AIContext) -> AIState:
        """
        Determines the next state based on strict priority.
        1. Emergency
        2. Battery Critical
        3. Hazard
        4. Navigation Blocked
        5. Goal Reached
        6. Exploration
        7. Idle
        """
        if context.emergency_active:
            return AIState.EMERGENCY
            
        if context.battery_critical:
            return AIState.RETURNING
            
        if context.threat_level in ["HIGH", "CRITICAL"]:
            return AIState.AVOIDING
            
        if context.navigation_blocked:
            return AIState.SCANNING # Could also be AVOIDING depending on logic
            
        if context.goal_reached:
            return AIState.IDLE
            
        if not context.is_paused:
            # If no override condition, keep exploring if there is an objective
            if context.current_objective != "None":
                return AIState.EXPLORING
            else:
                return AIState.IDLE
                
        return AIState.PAUSED
