"""
decision_planner.py
Recon Rover V1 - Decision Interpretation & Action Planning

Generates structured, immutable execution plans.
"""

from dataclasses import dataclass, field
from typing import List
import time

@dataclass
class ActionPlan:
    plan_id: str
    timestamp: float
    priority: int # 0=Lowest, 100=Emergency
    immediate_action: str
    short_term_actions: List[str] = field(default_factory=list)
    long_term_goals: List[str] = field(default_factory=list)
    reasoning: str = ""

class DecisionPlanner:
    def __init__(self):
        self._plan_counter = 0

    def generate_plan(self, final_intent: str, priority_score: int, reasoning: str, mission_rec: str) -> ActionPlan:
        self._plan_counter += 1
        
        # Simple structuring logic for Phase 5.7
        # In a full ROS2 system, this would map to Navigation2 waypoints
        return ActionPlan(
            plan_id=f"PLAN_{int(time.time())}_{self._plan_counter}",
            timestamp=time.time(),
            priority=priority_score,
            immediate_action=final_intent,
            short_term_actions=[],
            long_term_goals=[mission_rec] if mission_rec else [],
            reasoning=reasoning
        )
