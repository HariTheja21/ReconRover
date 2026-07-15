from typing import Any
import asyncio

from .demo_events import MissionDemoStarted, MissionDemoCompleted, MissionDemoFailed, SystemReady, SystemShutdown, FinalPerformanceReport
from .demo_bridge import DemoBridge
from .demo_health import DemoHealth
from .demo_statistics import DemoStatistics

from .startup_sequence import StartupSequence
from .shutdown_sequence import ShutdownSequence
from .system_readiness import SystemReadiness
from .recovery_manager import RecoveryManager
from .mission_validator import MissionValidator
from .integration_coordinator import IntegrationCoordinator
from .demo_logger import DemoLogger
from .demo_report import DemoReport
from .demo_scenario import DemoScenario
from .scenario_manager import ScenarioManager
from .mission_demo import MissionDemo
from .demo_manager import DemoManager
from .demo_scheduler import DemoScheduler

class DemoRuntime:
    def __init__(self, event_bus: Any):
        self.bridge = DemoBridge(event_bus)
        self.health = DemoHealth()
        self.stats = DemoStatistics()
        
        self.startup = StartupSequence()
        self.shutdown = ShutdownSequence()
        self.readiness = SystemReadiness()
        self.recovery = RecoveryManager()
        self.validator = MissionValidator()
        self.coordinator = IntegrationCoordinator()
        self.logger = DemoLogger()
        self.report = DemoReport()
        self.scenario_gen = DemoScenario()
        
        self.scenario_mgr = ScenarioManager(self.scenario_gen)
        self.mission = MissionDemo(self.coordinator, self.logger)
        
        self.manager = DemoManager(
            self.bridge, self.startup, self.shutdown, self.readiness, 
            self.recovery, self.validator, self.scenario_mgr, 
            self.mission, self.report
        )
        self.scheduler = DemoScheduler(self.manager)
        
    async def initialize(self):
        return True
