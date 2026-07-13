"""
execution_dispatcher.py
Recon Rover V1 - Action Execution Orchestrator

Responsible for broadcasting the ExecutionRequest to the EventBus.
"""

from event_bus import EventBus, ExecutionRequest

class ExecutionDispatcher:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        
    def dispatch(self, plan_data: dict):
        self.event_bus.publish(ExecutionRequest(
            plan_id=plan_data["plan_id"],
            priority=plan_data["priority"],
            action=plan_data["immediate_action"]
        ))
