"""
decision_interpreter.py
Recon Rover V1 - Decision Interpretation & Action Planning

Normalizes the raw intent strings from the LLM.
"""

from dataclasses import dataclass

@dataclass
class InterpretedIntent:
    movement: str
    priority_label: str
    reasoning: str
    mission_rec: str

class DecisionInterpreter:
    def interpret(self, movement_intent: str, priority: str, reasoning: str, mission_rec: str) -> InterpretedIntent:
        # Standardize strings just in case the LLM used lowercase or trailing spaces
        move = movement_intent.upper().strip()
        pri = priority.upper().strip()
        
        valid_moves = {"FORWARD", "BACKWARD", "LEFT", "RIGHT", "STOP"}
        if move not in valid_moves:
            move = "STOP"
            
        return InterpretedIntent(
            movement=move,
            priority_label=pri,
            reasoning=reasoning,
            mission_rec=mission_rec
        )
