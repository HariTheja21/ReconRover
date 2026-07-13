"""
ai_statistics.py
Recon Rover V1 - AI Decision Engine

Tracks long-term operational statistics.
"""

from dataclasses import dataclass
import time

@dataclass
class AIStatsSnapshot:
    decisions_per_sec: float = 0.0
    goal_changes: int = 0
    emergency_count: int = 0
    exploration_time_sec: float = 0.0
    pause_duration_sec: float = 0.0
    hazard_responses: int = 0
    return_home_count: int = 0

class AIStatistics:
    def __init__(self):
        self._start_time = time.time()
        self.decision_count = 0
        self.goal_changes = 0
        self.emergency_count = 0
        self.hazard_responses = 0
        self.return_home_count = 0
        
        self._state_start_times = {}
        self._state_durations = {"EXPLORING": 0.0, "PAUSED": 0.0}
        self._current_tracked_state = None

    def record_decision(self):
        self.decision_count += 1

    def record_goal_change(self):
        self.goal_changes += 1

    def record_emergency(self):
        self.emergency_count += 1

    def record_hazard_response(self):
        self.hazard_responses += 1

    def record_return_home(self):
        self.return_home_count += 1

    def track_state_duration(self, state_name: str):
        now = time.time()
        
        if self._current_tracked_state and self._current_tracked_state in self._state_durations:
            elapsed = now - self._state_start_times.get(self._current_tracked_state, now)
            self._state_durations[self._current_tracked_state] += elapsed
            
        self._current_tracked_state = state_name
        self._state_start_times[state_name] = now

    def get_snapshot(self) -> AIStatsSnapshot:
        # Update running duration
        self.track_state_duration(self._current_tracked_state)
        
        now = time.time()
        elapsed = max(now - self._start_time, 1.0)
        
        return AIStatsSnapshot(
            decisions_per_sec=self.decision_count / elapsed,
            goal_changes=self.goal_changes,
            emergency_count=self.emergency_count,
            exploration_time_sec=self._state_durations.get("EXPLORING", 0.0),
            pause_duration_sec=self._state_durations.get("PAUSED", 0.0),
            hazard_responses=self.hazard_responses,
            return_home_count=self.return_home_count
        )
