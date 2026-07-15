"""
Task Executor Module
Recon Rover V2 - Phase 3.9
"""
from typing import Any
from .task_library import create_task

class TaskExecutor:
    """Instantiates and monitors a specific task."""
    def __init__(self, event_bus: Any):
        self.bus = event_bus
        self.active_task = None
        
    def start_task(self, task_def: dict, mission_id: str, index: int) -> bool:
        try:
            self.active_task = create_task(task_def['type'], task_def.get('args', {}), self.bus)
            self.active_task.start(mission_id, index)
            return True
        except Exception as e:
            print(f"Task Start Failed: {e}")
            return False
            
    def tick(self, context: Any) -> str:
        """Returns 'RUNNING', 'COMPLETED', 'FAILED', or 'NONE'"""
        if not self.active_task:
            return "NONE"
        return self.active_task.check_status(context)
        
    def clear(self):
        self.active_task = None
