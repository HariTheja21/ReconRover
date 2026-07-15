"""
Avoidance Events Module
Recon Rover V2 - Phase 3.8
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class SafeTrajectoryGenerated(Event):
    timestamp: float
    trajectory: List[Tuple[float, float]]
    speed: float

@dataclass
class ObstacleAvoided(Event):
    timestamp: float

@dataclass
class CollisionPredicted(Event):
    timestamp: float
    time_to_collision: float
    distance_cm: float

@dataclass
class EmergencyStopRequired(Event):
    timestamp: float
    reason: str

@dataclass
class AvoidanceHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]

@dataclass
class AvoidanceStatisticsUpdated(Event):
    timestamp: float
    collisions_predicted: int
    stops_triggered: int
