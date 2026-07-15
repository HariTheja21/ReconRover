"""
Navigation Events Module
Recon Rover V2 - Phase 3.6
"""
from dataclasses import dataclass
from typing import Dict, Any, List

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class NavigationStateUpdated(Event):
    timestamp: float
    state: str # e.g. IDLE, NAVIGATING, REACHED
    current_target: tuple

@dataclass
class GoalReached(Event):
    timestamp: float
    goal_id: str
    target_pose: tuple

@dataclass
class WaypointReached(Event):
    timestamp: float
    waypoint_index: int
    waypoint_pose: tuple

@dataclass
class NavigationHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]

# Input events (Stubs for testing if not existing)
@dataclass
class MissionUpdated(Event):
    mission_id: str
    command: str

@dataclass
class GoalUpdated(Event):
    goal_id: str
    target_x: float
    target_y: float
