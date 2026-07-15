from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class MissionCreatedEvent:
    mission_id: str
    name: str
    waypoints: List[Dict[str, Any]]
    timestamp: float

@dataclass
class MissionExecutionRequestEvent:
    mission_id: str
    client_id: str
    timestamp: float

@dataclass
class MissionStatusEvent:
    mission_id: str
    status: str # PENDING, RUNNING, PAUSED, COMPLETED, CANCELLED, FAILED
    progress: float
    current_waypoint_index: int
    timestamp: float
