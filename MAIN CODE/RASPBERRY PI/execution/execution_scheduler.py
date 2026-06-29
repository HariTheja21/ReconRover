"""
execution_scheduler.py
Recon Rover V1 - Action Execution Orchestrator

Manages the logical sequencing of the queue.
"""

from .execution_queue import ExecutionQueue
from .execution_context import ExecutionContext

class ExecutionScheduler:
    def __init__(self, queue: ExecutionQueue, context: ExecutionContext):
        self.queue = queue
        self.context = context
        
    def get_next_action(self) -> dict:
        """Pops the highest priority valid plan from the queue."""
        
        # If E-Stop is active, flush the queue to prevent a backlog
        # of actions suddenly executing when E-Stop clears.
        if self.context.emergency_stop_active:
            self.queue.flush()
            return None
            
        plan = self.queue.pop_plan()
        return plan
