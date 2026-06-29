"""
mission_statistics.py
Recon Rover V1 - Mission Manager

Tracks long-term statistics for the mission manager.
"""

from dataclasses import dataclass
import time

@dataclass
class MissionStatsSnapshot:
    total_missions: int = 0
    completed_missions: int = 0
    failed_missions: int = 0
    cancelled_missions: int = 0
    timeouts: int = 0
    emergency_activations: int = 0
    manual_overrides: int = 0
    scheduler_decisions: int = 0
    uptime_sec: float = 0.0

class MissionStatistics:
    def __init__(self):
        self._start_time = time.time()
        self._total_missions = 0
        self._completed_missions = 0
        self._failed_missions = 0
        self._cancelled_missions = 0
        self._timeouts = 0
        self._emergency_activations = 0
        self._manual_overrides = 0
        self._scheduler_decisions = 0

    def record_mission_start(self, mission_type: str):
        self._total_missions += 1
        if mission_type == "Emergency Stop":
            self._emergency_activations += 1
        elif mission_type == "Manual Override":
            self._manual_overrides += 1

    def record_mission_completed(self):
        self._completed_missions += 1

    def record_mission_failed(self):
        self._failed_missions += 1

    def record_mission_cancelled(self):
        self._cancelled_missions += 1

    def record_timeout(self):
        self._timeouts += 1
        
    def record_scheduler_decision(self):
        self._scheduler_decisions += 1

    def get_snapshot(self) -> MissionStatsSnapshot:
        now = time.time()
        elapsed = max(now - self._start_time, 1.0)
        
        return MissionStatsSnapshot(
            total_missions=self._total_missions,
            completed_missions=self._completed_missions,
            failed_missions=self._failed_missions,
            cancelled_missions=self._cancelled_missions,
            timeouts=self._timeouts,
            emergency_activations=self._emergency_activations,
            manual_overrides=self._manual_overrides,
            scheduler_decisions=self._scheduler_decisions,
            uptime_sec=elapsed
        )
