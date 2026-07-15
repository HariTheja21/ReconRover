from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class FrontierDetected:
    frontiers: List[Dict[str, Any]]
    timestamp: float

@dataclass
class ExplorationGoalSelected:
    goal_x: float
    goal_y: float
    rank_score: float
    timestamp: float

@dataclass
class ExplorationMissionGenerated:
    mission_id: str
    target_x: float
    target_y: float
    priority: int
    timestamp: float

@dataclass
class CoverageUpdated:
    explored_area_m2: float
    coverage_percentage: float
    timestamp: float

@dataclass
class DeadlockDetected:
    deadlock_reason: str
    time_in_deadlock: float
    timestamp: float

@dataclass
class RecoveryRequested:
    recovery_strategy: str
    target_x: float
    target_y: float
    timestamp: float

@dataclass
class ExplorationStateUpdated:
    state: str
    timestamp: float
