"""
ai_health.py
Recon Rover V1 - AI Decision Engine

Tracks internal health metrics for the cognitive layer.
"""

from dataclasses import dataclass

@dataclass
class AIHealthMetrics:
    decision_count: int = 0
    transition_count: int = 0
    invalid_transitions: int = 0
    total_decision_time_ms: float = 0.0
    worst_decision_time_ms: float = 0.0
    current_state: str = "IDLE"
    current_goal: str = "None"
    confidence: float = 1.0

class AIHealth:
    def __init__(self):
        self.metrics = AIHealthMetrics()

    def record_decision(self, duration_ms: float):
        self.metrics.decision_count += 1
        self.metrics.total_decision_time_ms += duration_ms
        if duration_ms > self.metrics.worst_decision_time_ms:
            self.metrics.worst_decision_time_ms = duration_ms

    def record_transition(self, is_valid: bool):
        if is_valid:
            self.metrics.transition_count += 1
        else:
            self.metrics.invalid_transitions += 1

    def update_state(self, state: str, goal: str, confidence: float):
        self.metrics.current_state = state
        self.metrics.current_goal = goal
        self.metrics.confidence = confidence
        
    def get_average_decision_time(self) -> float:
        if self.metrics.decision_count == 0:
            return 0.0
        return self.metrics.total_decision_time_ms / self.metrics.decision_count
