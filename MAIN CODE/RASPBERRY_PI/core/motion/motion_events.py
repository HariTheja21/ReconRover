"""
Motion Events Module
Recon Rover V2 - Phase 4.0
"""
from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class MotionRequest(Event):
    timestamp: float
    linear_velocity: float  # Normalized [-1.0, 1.0]
    angular_velocity: float # Normalized [-1.0, 1.0]
    
@dataclass
class MotionStopped(Event):
    timestamp: float
    reason: str

@dataclass
class MotionPaused(Event):
    timestamp: float

@dataclass
class MotionResumed(Event):
    timestamp: float

@dataclass
class MotionStateUpdated(Event):
    timestamp: float
    state: str

@dataclass
class MotionHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]

@dataclass
class MotionStatisticsUpdated(Event):
    timestamp: float
    requests_processed: int
    limits_applied: int
