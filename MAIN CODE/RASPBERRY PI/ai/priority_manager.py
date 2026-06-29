"""
priority_manager.py
Recon Rover V1 - AI Decision Engine

Resolves conflicts between candidate actions.
Hierarchy: Emergency > Battery > Obstacle > Mission > Exploration
"""

from typing import List
from .ai_blackboard import CandidateAction

class PriorityManager:
    def resolve(self, actions: List[CandidateAction]) -> CandidateAction:
        """Returns the highest priority action."""
        if not actions:
            return CandidateAction(intent="Idle", priority_score=0, source="priority_manager")
            
        # Sort descending by priority_score
        sorted_actions = sorted(actions, key=lambda a: a.priority_score, reverse=True)
        return sorted_actions[0]
