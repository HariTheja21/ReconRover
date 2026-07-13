"""
autonomy_monitor.py
Recon Rover V1 - Autonomous Intelligence

Observes objective failures and timeouts.
"""

import time
from event_bus import EventBus, ObjectiveFailed
from .autonomy_objectives import AutonomyObjectives

class AutonomyMonitor:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.objective_start_times = {}

    def track_start(self, objective: str):
        self.objective_start_times[objective] = time.perf_counter()

    def check_timeouts(self, active_objective: str, objectives_manager: AutonomyObjectives, timeout_sec: float = 60.0):
        if not active_objective or active_objective == "IDLE":
            return
            
        start_time = self.objective_start_times.get(active_objective)
        if start_time and (time.perf_counter() - start_time) > timeout_sec:
            # Emit failure to force replan
            self.event_bus.publish(ObjectiveFailed(
                objective=active_objective,
                reason="Timeout"
            ))
            
            # Clear it so the scheduler picks a new one
            if active_objective in objectives_manager.temporary_objectives:
                objectives_manager.temporary_objectives.remove(active_objective)
            if active_objective in objectives_manager.emergency_objectives:
                objectives_manager.emergency_objectives.remove(active_objective)
