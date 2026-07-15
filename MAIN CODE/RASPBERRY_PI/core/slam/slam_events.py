"""
SLAM Events Module
Recon Rover V2 - Phase 3.5
"""
from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class CorrectedPoseUpdated(Event):
    timestamp: float
    x: float
    y: float
    theta: float
    confidence: float

@dataclass
class SLAMMapUpdated(Event):
    timestamp: float
    alignment_score: float

@dataclass
class LoopClosureDetected(Event):
    timestamp: float
    matched_pose: tuple
    correction_delta: tuple

@dataclass
class SLAMStatisticsUpdated(Event):
    timestamp: float
    matches_performed: int
    loop_closures_found: int

@dataclass
class SLAMHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]
