"""
Fusion Events Module
Recon Rover V2 - Phase 3.2
"""
from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class FusedObstacle(Event):
    timestamp: float
    distance_cm: float
    threat_level: str
    confidence: float
    contributing_sensors: list

@dataclass
class FusedDistance(Event):
    timestamp: float
    distance_cm: float
    confidence: float
    contributing_sensors: list

@dataclass
class FusedOrientation(Event):
    timestamp: float
    pitch: float
    roll: float
    yaw: float
    confidence: float

@dataclass
class SensorConfidenceUpdated(Event):
    timestamp: float
    sensor_id: str
    confidence: float
    reason: str

@dataclass
class EnvironmentUpdated(Event):
    timestamp: float
    active_fusions: int

@dataclass
class FusionHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]
