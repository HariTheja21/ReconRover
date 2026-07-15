import asyncio
from typing import Any
from .executive_health import ExecutiveHealth
from .executive_statistics import ExecutiveStatistics
from .executive_bridge import ExecutiveBridge
from .mission_context import MissionContext
from .mission_state_machine import MissionStateMachine
from .objective_manager import ObjectiveManager
from .objective_scheduler import ObjectiveScheduler
from .mission_supervisor import MissionSupervisor
from .mission_monitor import MissionMonitor
from .decision_coordinator import DecisionCoordinator
from .resource_allocator import ResourceAllocator
from .policy_engine import PolicyEngine
from .priority_manager import PriorityManager
from .risk_assessor import RiskAssessor
from .mission_logger import MissionLogger
from .mission_recovery import MissionRecovery
from .mission_executive import MissionExecutive
from .executive_api import ExecutiveAPI
from .executive_engine import ExecutiveEngine
from .executive_scheduler import ExecutiveScheduler

class ExecutiveManager:
    def __init__(self, event_bus: Any):
        self.health = ExecutiveHealth()
        self.stats = ExecutiveStatistics()
        self.bridge = ExecutiveBridge(event_bus)
        
        # Core components
        self.ctx = MissionContext()
        self.sm = MissionStateMachine()
        self.om = ObjectiveManager()
        self.os = ObjectiveScheduler(self.om)
        self.sup = MissionSupervisor()
        self.mon = MissionMonitor()
        self.coord = DecisionCoordinator(self.bridge.publish_event)
        self.alloc = ResourceAllocator()
        self.policy = PolicyEngine()
        self.prio = PriorityManager()
        self.risk = RiskAssessor()
        self.logger = MissionLogger()
        self.recovery = MissionRecovery(self.bridge.publish_event)
        
        self.mission_exec = MissionExecutive(
            self.ctx, self.sm, self.om, self.sup, self.mon,
            self.coord, self.alloc, self.policy, self.prio, self.risk,
            self.logger, self.recovery, self.stats, self.bridge.publish_event
        )
        
        self.api = ExecutiveAPI(self.mission_exec)
        self.engine = ExecutiveEngine(self.mission_exec, self.api)
        self.scheduler = ExecutiveScheduler(self.engine)
        
    async def start(self):
        asyncio.create_task(self.scheduler.run_executive_loop())
