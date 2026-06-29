"""
autonomy_coordinator.py
Recon Rover V1 - Autonomous Intelligence

Coordinates subsystem requirements for the scheduled objective.
"""

from .autonomy_blackboard import AutonomyBlackboard

class AutonomyCoordinator:
    def coordinate(self, blackboard: AutonomyBlackboard):
        """Identifies subsystem constraints required for the objective."""
        
        if blackboard.selected_objective == "SYSTEM_HALT":
            blackboard.coordinator_constraints.append("DISABLE_NAVIGATION")
            
        elif blackboard.selected_objective == "RETURN_TO_BASE":
            blackboard.coordinator_constraints.append("PRIORITIZE_NAVIGATION")
            blackboard.coordinator_constraints.append("SUSPEND_LLM")
            
        elif blackboard.selected_objective == "EXPLORE":
            blackboard.coordinator_constraints.append("ACTIVATE_VISION")
            blackboard.coordinator_constraints.append("ACTIVATE_LLM")
