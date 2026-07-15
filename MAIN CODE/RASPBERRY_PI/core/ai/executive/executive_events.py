from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class MissionStarted:
    mission_id: str
    timestamp: float

@dataclass
class MissionPaused:
    mission_id: str
    reason: str
    timestamp: float

@dataclass
class MissionResumed:
    mission_id: str
    timestamp: float

@dataclass
class MissionCompleted:
    mission_id: str
    timestamp: float

@dataclass
class MissionFailed:
    mission_id: str
    reason: str
    timestamp: float

@dataclass
class MissionRecovered:
    mission_id: str
    timestamp: float

@dataclass
class ExecutiveDecisionGenerated:
    decision_id: str
    action: str
    timestamp: float
