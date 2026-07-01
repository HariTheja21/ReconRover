"""
rule_engine.py
Recon Rover V1 - AI Decision Engine

Enforces strict deterministic constraints on candidate actions.
"""

from .ai_context import AIContext
from .ai_blackboard import AIBlackboard, CandidateAction

class RuleEngine:
    def enforce(self, context: AIContext, blackboard: AIBlackboard):
        """Filters candidate actions or injects emergency overrides."""
        
        # 1. Hardware Fault Override
        if context.system_health != "OK":
            blackboard.rule_overrides.append("SYSTEM_FAULT")
            blackboard.filtered_actions.append(
                CandidateAction(intent="EmergencyStop", source="rule_engine", priority_score=200)
            )
            return
            
        # 2. Critical Battery Override
        if context.battery_critical:
            blackboard.rule_overrides.append("BATTERY_CRITICAL")
            blackboard.filtered_actions.append(
                CandidateAction(intent="ReturnHome", source="rule_engine", priority_score=100)
            )
            return  # Drop all other candidates

        # 3. Hazard Avoidance Override
        if context.hazard_detected:
            blackboard.rule_overrides.append("HAZARD_AVOIDANCE")
            blackboard.filtered_actions.append(
                CandidateAction(intent="AvoidHazard", source="rule_engine", priority_score=150)
            )
            return

        # 4. Obstacle Avoidance Override
        if context.obstacle_detected:
            blackboard.rule_overrides.append("OBSTACLE_AVOIDANCE")
            blackboard.filtered_actions.append(
                CandidateAction(intent="AvoidObstacle", source="rule_engine", priority_score=120)
            )
            return

        # Pass through candidates if no rules triggered
        blackboard.filtered_actions.extend(blackboard.candidate_actions)
