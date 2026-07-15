"""
World Events Module
Recon Rover V2 - Phase 3.1
"""
from dataclasses import dataclass
from typing import Dict, Any, List

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

# Subscribed Events (Defined in Sensor layer, re-declaring types for reference)
@dataclass
class IMUUpdated(Event): pass
@dataclass
class DistanceUpdated(Event): pass
@dataclass
class ObstacleDetected(Event): pass
@dataclass
class BatteryUpdated(Event): pass
@dataclass
class CameraFrameAvailable(Event): pass

# Published Events
@dataclass
class WorldUpdated(Event):
    timestamp: float
    entity_count: int
    obstacle_count: int
    landmark_count: int
    
@dataclass
class ObstacleMapUpdated(Event):
    timestamp: float
    active_obstacles: List[Dict[str, Any]]
    
@dataclass
class LandmarkUpdated(Event):
    timestamp: float
    landmark_id: str
    semantic_class: str
    confidence: float
    
@dataclass
class RobotStateUpdated(Event):
    timestamp: float
    battery_percentage: float
    pitch: float
    roll: float
    yaw: float
    
@dataclass
class WorldHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]
