"""
autonomy_supervisor.py
Recon Rover V1 - Autonomous Intelligence

Guarantees subsystem cooperation and acts as a fail-safe.
"""

from .autonomy_context import AutonomyContext
from .autonomy_blackboard import AutonomyBlackboard

class AutonomySupervisor:
    def supervise(self, context: AutonomyContext, blackboard: AutonomyBlackboard):
        """Prevents subsystem conflicts."""
        
        # Cannot run heavy LLM inference if battery is critical
        if context.battery_critical and "ACTIVATE_LLM" in blackboard.coordinator_constraints:
            blackboard.supervisor_overrides.append("OVERRIDE_SUSPEND_LLM")
            
        # Cannot navigate if hardware fault detected
        if context.health_status != "OK" and blackboard.selected_objective != "SYSTEM_HALT":
            blackboard.supervisor_overrides.append("FORCE_SYSTEM_HALT")
            blackboard.selected_objective = "SYSTEM_HALT"
