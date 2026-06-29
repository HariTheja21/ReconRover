"""
decision_validator.py
Recon Rover V1 - Decision Interpretation & Action Planning

Validates logical consistency between the LLM decision and current state.
"""

from .decision_context import DecisionContext
from .decision_interpreter import InterpretedIntent

class DecisionValidator:
    def validate(self, intent: InterpretedIntent, context: DecisionContext) -> bool:
        """
        Returns True if the intent is logically valid, False if it's contradictory.
        """
        # Example validation: You cannot move FORWARD if you are already BLOCKED
        if intent.movement == "FORWARD" and context.nav_state == "BLOCKED_FRONT":
            return False
            
        # Example validation: You cannot turn LEFT if you are BLOCKED_LEFT
        if intent.movement == "LEFT" and context.nav_state == "BLOCKED_LEFT":
            return False
            
        return True
