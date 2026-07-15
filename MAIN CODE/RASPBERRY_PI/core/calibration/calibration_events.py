from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CalibrationStartedEvent:
    timestamp: float

@dataclass
class DeviceMappedEvent:
    logical_name: str
    physical_path: str

@dataclass
class ComponentCalibratedEvent:
    component: str
    parameters: Dict[str, Any]

@dataclass
class CalibrationFailedEvent:
    component: str
    reason: str

@dataclass
class CalibrationCompletedEvent:
    profile_path: str
    total_time_ms: int
