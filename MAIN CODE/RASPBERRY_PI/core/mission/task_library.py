"""
Task Library Module
Recon Rover V2 - Phase 3.9
"""
from typing import Any
try:
    from core.navigation.navigation_events import GoalUpdated
except ImportError:
    from dataclasses import dataclass
    @dataclass
    class GoalUpdated:
        goal_id: str; target_x: float; target_y: float

class BaseTask:
    def __init__(self, event_bus: Any, args: dict):
        self.bus = event_bus
        self.args = args

    def start(self, mission_id: str, task_index: int):
        raise NotImplementedError

    def check_status(self, context: Any) -> str:
        """Returns 'RUNNING', 'COMPLETED', or 'FAILED'"""
        raise NotImplementedError

class NavigateToTask(BaseTask):
    def start(self, mission_id: str, task_index: int):
        x = self.args.get('x', 0.0)
        y = self.args.get('y', 0.0)
        gid = f"{mission_id}_t{task_index}"
        self.bus.publish(GoalUpdated(goal_id=gid, target_x=x, target_y=y))
        
    def check_status(self, context: Any) -> str:
        # Relies on the external 'goal_reached' flag set by MissionManager listening to GoalReached event
        if context.get("goal_reached"):
            return "COMPLETED"
        if context.get("emergency_stop"):
            return "FAILED"
        return "RUNNING"

class WaitTask(BaseTask):
    def start(self, mission_id: str, task_index: int):
        import time
        self.end_time = time.time() + self.args.get('duration_s', 1.0)
        
    def check_status(self, context: Any) -> str:
        import time
        if time.time() >= getattr(self, 'end_time', 0):
            return "COMPLETED"
        return "RUNNING"

# Factory
def create_task(task_type: str, args: dict, bus: Any) -> BaseTask:
    registry = {
        "NavigateTo": NavigateToTask,
        "Wait": WaitTask
    }
    cls = registry.get(task_type)
    if cls:
        return cls(bus, args)
    raise ValueError(f"Unknown task type: {task_type}")
