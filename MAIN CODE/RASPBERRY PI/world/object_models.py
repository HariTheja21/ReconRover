"""
object_models.py
Recon Rover V1 - Cognitive Layer

Data structures representing abstract world entities.
"""

from dataclasses import dataclass
from enum import Enum

class CellState(Enum):
    UNKNOWN = 0
    FREE = 1
    OBSTACLED = 2

@dataclass
class SpatialCell:
    state: CellState = CellState.UNKNOWN
    distance_cm: float = -1.0
    confidence: float = 0.0
    last_updated_ms: int = 0

@dataclass
class Obstacle:
    location: str  # "front", "left", "right", "rear"
    distance_cm: float
    confidence: float
    timestamp_ms: int

@dataclass
class Hazard:
    hazard_type: str  # "gas"
    severity: float   # 0.0 to 1.0
    confidence: float
    timestamp_ms: int

@dataclass
class RoverPose:
    pitch: float = 0.0
    roll: float = 0.0
    yaw: float = 0.0
