"""
world_state.py
Recon Rover V1 - Cognitive Layer

The unified representation of the Rover's understanding of the world.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from .object_models import RoverPose, SpatialCell, Hazard

@dataclass
class BatteryState:
    percentage: float = 0.0
    voltage: float = 0.0
    is_critical: bool = False

@dataclass
class WorldState:
    timestamp_ms: int = 0
    pose: RoverPose = field(default_factory=RoverPose)
    
    # Simple spatial memory mapping cardinal directions to a Cell
    spatial_grid: Dict[str, SpatialCell] = field(default_factory=lambda: {
        "front": SpatialCell(),
        "left": SpatialCell(),
        "right": SpatialCell(),
        "rear": SpatialCell()
    })
    
    # Tracking active hazards
    active_hazards: List[Hazard] = field(default_factory=list)
    
    battery: BatteryState = field(default_factory=BatteryState)
    
    # Classification: "SAFE", "WARNING", "CRITICAL"
    threat_level: str = "UNKNOWN"
    
    # Confidence of the overall world model
    confidence: float = 0.0
    
    # Navigation Hint: Where is it safest to move?
    last_known_safe_direction: str = "UNKNOWN"
