"""
confidence_engine.py
Recon Rover V1 - AI Decision Engine

Calculates a normalized confidence score for the selected action.
"""

from .ai_blackboard import CandidateAction

class ConfidenceEngine:
    def calculate(self, action: CandidateAction) -> float:
        """
        Determines how confident the AI is in this action.
        Currently a stub. In the future, this will fuse ML confidence scores
        (e.g., Vision Object probability * Audio Speech probability).
        """
        if action.intent in ["EmergencyStop", "ReturnHome"]:
            return 1.0  # Rule-based overrides have 100% confidence
            
        # Stub default for normal reasoning candidates
        return 0.85
