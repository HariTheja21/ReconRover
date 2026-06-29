"""
decision_manager.py
Recon Rover V1 - Decision Interpretation & Action Planning

Coordinates the full validation and planning pipeline.
"""

from typing import Optional
from .decision_context import DecisionContext
from .decision_interpreter import DecisionInterpreter
from .decision_validator import DecisionValidator
from .decision_safety import DecisionSafety
from .decision_prioritizer import DecisionPrioritizer
from .decision_planner import DecisionPlanner, ActionPlan
from .decision_health import DecisionHealth
from .decision_statistics import DecisionStatistics

class DecisionManager:
    def __init__(self):
        self.context = DecisionContext()
        self.interpreter = DecisionInterpreter()
        self.validator = DecisionValidator()
        self.safety = DecisionSafety()
        self.prioritizer = DecisionPrioritizer()
        self.planner = DecisionPlanner()
        
        self.health = DecisionHealth()
        self.stats = DecisionStatistics()

    def build_plan_from_llm(self, movement: str, priority: str, reasoning: str, mission_rec: str) -> Optional[ActionPlan]:
        """Runs the validation funnel and outputs an ActionPlan if safe."""
        
        # 1. Interpret
        intent = self.interpreter.interpret(movement, priority, reasoning, mission_rec)
        
        # 2. Validate basic logic
        if not self.validator.validate(intent, self.context):
            self.health.record_rejection()
            return None # Logically invalid, wait for next LLM cycle
            
        # 3. Apply Hard Safety Constraints
        safe_move = self.safety.check_safety_override(intent.movement, self.context)
        if safe_move != intent.movement:
            self.health.record_safety_veto()
            
        # 4. Prioritize
        final_priority = self.prioritizer.assign_priority(intent.priority_label, safe_move, self.context)
        
        # 5. Generate Plan
        plan = self.planner.generate_plan(
            final_intent=safe_move,
            priority_score=final_priority,
            reasoning=intent.reasoning,
            mission_rec=intent.mission_rec
        )
        
        self.stats.record_plan()
        return plan
