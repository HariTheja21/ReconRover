import asyncio
from typing import Any
from .planner_health import PlannerHealth
from .planner_statistics import PlannerStatistics
from .planner_bridge import PlannerBridge
from .behavior_executor import BehaviorExecutor
from .goal_manager import GoalManager
from .mission_manager import MissionManager
from .task_queue import TaskQueue
from .task_executor import TaskExecutor
from .task_monitor import TaskMonitor
from .failure_manager import FailureManager
from .recovery_planner import RecoveryPlanner
from .plan_optimizer import PlanOptimizer
from .task_planner_engine import TaskPlannerEngine
from .task_scheduler import TaskScheduler

class TaskPlannerManager:
    def __init__(self, event_bus: Any):
        self.health = PlannerHealth()
        self.stats = PlannerStatistics()
        self.bridge = PlannerBridge(event_bus)
        
        # Subcomponents
        self.be = BehaviorExecutor()
        self.gm = GoalManager()
        self.mm = MissionManager()
        self.tq = TaskQueue()
        self.te = TaskExecutor()
        self.tm = TaskMonitor()
        self.fm = FailureManager()
        self.rp = RecoveryPlanner()
        self.po = PlanOptimizer()
        
        # Assembly
        self.engine = TaskPlannerEngine(
            self.be, self.gm, self.mm, self.tq, self.te, self.tm,
            self.fm, self.rp, self.po, self.stats, self.bridge.publish_event
        )
        
        self.scheduler = TaskScheduler(self.engine)
        
    async def start(self):
        asyncio.create_task(self.scheduler.run_mission_loop())
        asyncio.create_task(self.scheduler.run_task_loop())
