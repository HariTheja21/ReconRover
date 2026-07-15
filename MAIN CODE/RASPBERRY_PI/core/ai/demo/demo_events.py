from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class MissionDemoStarted:
    scenario_id: str
    timestamp: float

@dataclass
class MissionDemoCompleted:
    scenario_id: str
    success: bool
    timestamp: float

@dataclass
class MissionDemoFailed:
    scenario_id: str
    reason: str
    timestamp: float

@dataclass
class SystemReady:
    subsystems_verified: int
    timestamp: float

@dataclass
class SystemShutdown:
    safe: bool
    timestamp: float

@dataclass
class FinalPerformanceReport:
    report: Dict[str, Any]
    timestamp: float
