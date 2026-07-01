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
        4. Obstacle / Nav Blocked
        5. Goal Reached
        6. Exploration
        7. Idle
        """
        if context.system_health != "OK":
            return AIState.EMERGENCY
            
        if context.battery_critical:
            return AIState.RETURNING
            
        if context.hazard_detected:
            return AIState.AVOIDING
            
        if context.obstacle_detected:
            return AIState.SCANNING
            
        if context.mission_state == "COMPLETED" or context.current_objective == "COMPLETED":
            return AIState.IDLE
            
        if context.current_objective != "IDLE" and context.current_objective != "None":
            return AIState.EXPLORING
            
        return AIState.IDLE
