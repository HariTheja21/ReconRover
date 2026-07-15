"""
Localization Events Module
Recon Rover V2 - Phase 3.3
"""
from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class RobotPoseUpdated(Event):
    timestamp: float
    x: float
    y: float
    theta: float
    confidence: float

@dataclass
class VelocityUpdated(Event):
    timestamp: float
    linear_velocity: float
    angular_velocity: float

@dataclass
class LocalizationUpdated(Event):
    timestamp: float
    pose_history_size: int

@dataclass
class LocalizationHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]
