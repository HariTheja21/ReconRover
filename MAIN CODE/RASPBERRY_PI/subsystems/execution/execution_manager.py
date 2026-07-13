"""
execution_manager.py
Recon Rover V1 - Action Execution Orchestrator

Coordinates the internal priority queue and dispatch logic.
"""

from event_bus import EventBus
from .execution_context import ExecutionContext
from .execution_queue import ExecutionQueue
from .execution_validator import ExecutionValidator
from .execution_scheduler import ExecutionScheduler
from .execution_dispatcher import ExecutionDispatcher
from .execution_monitor import ExecutionMonitor
from .execution_health import ExecutionHealth
from .execution_statistics import ExecutionStatistics

class ExecutionManager:
    def __init__(self, event_bus: EventBus):
        self.context = ExecutionContext()
        self.queue = ExecutionQueue()
        self.validator = ExecutionValidator()
        self.scheduler = ExecutionScheduler(self.queue, self.context)
        self.dispatcher = ExecutionDispatcher(event_bus)
        self.monitor = ExecutionMonitor()
        
        self.health = ExecutionHealth()
        self.stats = ExecutionStatistics()

    def process_new_plan(self, plan_id: str, priority: int, immediate_action: str, short_term_actions: list, long_term_goals: list):
        """Validates and queues an incoming plan."""
        
        if self.validator.validate_plan_for_queue(priority, immediate_action, self.context):
            self.queue.add_plan(plan_id, priority, immediate_action, short_term_actions, long_term_goals)
            self.monitor.mark_pending(plan_id)
            self.stats.record_queue()
        else:
            self.monitor.mark_cancelled(plan_id)
            self.health.record_cancellation()

    def tick(self):
        """Called repeatedly to pop the next plan and dispatch it."""
        plan_data = self.scheduler.get_next_action()
        if plan_data:
            self.dispatcher.dispatch(plan_data)
            self.monitor.mark_running(plan_data["plan_id"])
            self.stats.record_dispatch()
