"""
decision_engine.py
Recon Rover V1 - AI Decision Engine

Evaluates the remaining candidates and finalizes the decision via priority resolution.
"""

from .ai_blackboard import AIBlackboard
from .priority_manager import PriorityManager
from .confidence_engine import ConfidenceEngine

class DecisionEngine:
    def __init__(self):
        self.priority_manager = PriorityManager()
        self.confidence_engine = ConfidenceEngine()

    def decide(self, blackboard: AIBlackboard):
        """Picks the best action and calculates confidence."""
        
        # 1. Resolve Priority
        best_action = self.priority_manager.resolve(blackboard.filtered_actions)
        
        # 2. Calculate Confidence
        best_action.confidence = self.confidence_engine.calculate(best_action)
        
        # 3. Finalize
        blackboard.final_decision = best_action
