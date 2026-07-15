"""
Mission Events Module
Recon Rover V2 - Phase 3.9
"""
from dataclasses import dataclass
from typing import Dict, Any, List

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

# Input Requests
@dataclass
class MissionRequest(Event):
    timestamp: float
    mission_id: str
    priority: int
    tasks: List[dict] # Format: [{"type": "NavigateTo", "args": {"x": 10, "y": 20}}]

@dataclass
class MissionCancelledRequest(Event):
    timestamp: float
    mission_id: str

@dataclass
class MissionPauseRequest(Event):
    timestamp: float

@dataclass
class MissionResumeRequest(Event):
    timestamp: float

# Outputs
@dataclass
class MissionStarted(Event):
    timestamp: float
    mission_id: str

@dataclass
class MissionPaused(Event):
    timestamp: float
    mission_id: str

@dataclass
class MissionResumed(Event):
    timestamp: float
    mission_id: str

@dataclass
class MissionCompleted(Event):
    timestamp: float
    mission_id: str

@dataclass
class MissionFailed(Event):
    timestamp: float
    mission_id: str
    reason: str

@dataclass
class MissionCancelled(Event):
    timestamp: float
    mission_id: str

@dataclass
class TaskStarted(Event):
    timestamp: float
    mission_id: str
    task_index: int
    task_type: str

@dataclass
class TaskCompleted(Event):
    timestamp: float
    mission_id: str
    task_index: int

@dataclass
class TaskFailed(Event):
    timestamp: float
    mission_id: str
    task_index: int
    reason: str

@dataclass
class MissionHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]

@dataclass
class MissionStatisticsUpdated(Event):
    timestamp: float
    missions_completed: int
    missions_failed: int
    tasks_completed: int
