"""
autonomy_manager.py
Recon Rover V1 - Autonomous Intelligence

Coordinates the entire planning cycle for the Autonomy Engine.
"""

import time
from typing import Optional
from event_bus import EventBus
from .autonomy_context import AutonomyContext
from .autonomy_blackboard import AutonomyBlackboard
from .autonomy_objectives import AutonomyObjectives
from .autonomy_scheduler import AutonomyScheduler
from .autonomy_coordinator import AutonomyCoordinator
from .autonomy_supervisor import AutonomySupervisor
from .autonomy_executor import AutonomyExecutor
from .autonomy_monitor import AutonomyMonitor
from .autonomy_health import AutonomyHealth
from .autonomy_statistics import AutonomyStatistics

class AutonomyManager:
    def __init__(self, event_bus: EventBus):
        self.objectives = AutonomyObjectives()
        self.scheduler = AutonomyScheduler()
        self.coordinator = AutonomyCoordinator()
        self.supervisor = AutonomySupervisor()
        self.executor = AutonomyExecutor(event_bus)
        self.monitor = AutonomyMonitor(event_bus)
        self.health = AutonomyHealth()
        self.stats = AutonomyStatistics()

    def run_planning_cycle(self, context: AutonomyContext):
        """Executes a single tick of the autonomy brain."""
        self.stats.record_cycle()
        
        # 1. Instantiate short-lived blackboard
        blackboard = AutonomyBlackboard(timestamp=time.perf_counter())
        
        # 2. Schedule
        self.scheduler.schedule(context, blackboard, self.objectives)
        
        # 3. Coordinate constraints
        self.coordinator.coordinate(blackboard)
        
        # 4. Supervise safety
        self.supervisor.supervise(context, blackboard)
        
        # 5. Monitor timeouts
        if blackboard.selected_objective:
            self.monitor.check_timeouts(blackboard.selected_objective, self.objectives)
            
        # 6. Execute (publish semantic request)
        self.executor.execute(blackboard)
        
        self.health.record_success()
