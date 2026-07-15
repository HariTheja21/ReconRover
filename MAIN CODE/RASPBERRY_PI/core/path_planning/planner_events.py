"""
Path Planner Events Module
Recon Rover V2 - Phase 3.7
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class PathGenerated(Event):
    timestamp: float
    goal_id: str
    path: List[Tuple[float, float]]
    cost: float

@dataclass
class PathUpdated(Event):
    timestamp: float
    goal_id: str
    path: List[Tuple[float, float]]

@dataclass
class PathInvalidated(Event):
    timestamp: float
    reason: str

@dataclass
class PlannerHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]

@dataclass
class PlannerStatisticsUpdated(Event):
    timestamp: float
    paths_generated: int
    paths_optimized: int
