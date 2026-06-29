"""
execution_validator.py
Recon Rover V1 - Action Execution Orchestrator

Validates a plan against the execution context before it is added to the queue.
"""

from .execution_context import ExecutionContext

class ExecutionValidator:
    def validate_plan_for_queue(self, priority: int, immediate_action: str, context: ExecutionContext) -> bool:
        """
        Returns True if the plan is allowed to enter the queue.
        """
        # If an emergency stop is active, reject everything except an explicit STOP intent
        if context.emergency_stop_active and immediate_action != "STOP":
            return False
            
        # If battery is critical, only allow STOP or high priority overriding maneuvers
        if context.battery_critical and priority < 90 and immediate_action != "STOP":
            return False
            
        return True
