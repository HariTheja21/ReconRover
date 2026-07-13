"""
mission_health.py
Recon Rover V1 - Mission Manager

Tracks internal health metrics for the mission manager.
"""

from dataclasses import dataclass

@dataclass
class MissionHealthMetrics:
    current_mission: str = "None"
    scheduler_latency_ms: float = 0.0
    validation_failures: int = 0
    ownership_changes: int = 0

class MissionHealth:
    def __init__(self):
        self.metrics = MissionHealthMetrics()

    @property
    def current_mission(self) -> str:
        return self.metrics.current_mission
        
    @current_mission.setter
    def current_mission(self, value: str):
        self.metrics.current_mission = value

    @property
    def scheduler_latency_ms(self) -> float:
        return self.metrics.scheduler_latency_ms
        
    @scheduler_latency_ms.setter
    def scheduler_latency_ms(self, value: float):
        self.metrics.scheduler_latency_ms = value
        
    def record_validation_failure(self):
        self.metrics.validation_failures += 1
        
    def record_ownership_change(self):
        self.metrics.ownership_changes += 1
