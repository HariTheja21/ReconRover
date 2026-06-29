"""
autonomy_scheduler.py
Recon Rover V1 - Autonomous Intelligence

Chooses which objective to execute based on context.
"""

from .autonomy_context import AutonomyContext
from .autonomy_blackboard import AutonomyBlackboard
from .autonomy_objectives import AutonomyObjectives

class AutonomyScheduler:
    def schedule(self, context: AutonomyContext, blackboard: AutonomyBlackboard, objectives: AutonomyObjectives):
        """Selects the most pressing objective to fulfill."""
        
        # Pull candidate from AI/LLM layers first
        if context.ai_decision.get("intent") == "EmergencyStop":
            objectives.set_emergency_objective("SYSTEM_HALT")
        elif context.battery_critical:
            objectives.set_emergency_objective("RETURN_TO_BASE")
            
        blackboard.selected_objective = objectives.get_highest_priority()
