import asyncio
from typing import Any
from .task_planner_manager import TaskPlannerManager

class TaskPlannerRuntime:
    """
    Top-level facade for the Task Planner & Behavior Tree Engine.
    """
    def __init__(self, event_bus: Any):
        self.manager = TaskPlannerManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    async def ingest_mission(self, goal: str, params: dict):
        await self.manager.scheduler.enqueue_mission(goal, params)
        
    def cancel_active_mission(self):
        self.manager.tq.clear()
        self.manager.te.complete_task()
