from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SemanticObjectDetected:
    entity_id: str
    class_name: str
    confidence: float
    world_coords: List[float] # [x, y, z]
    distance_m: float
    timestamp: float

@dataclass
class SceneUpdated:
    scene_id: str
    entities: List[str]
    relationships: Dict[str, Any]
    timestamp: float

@dataclass
class EnvironmentUpdated:
    environment_type: str # e.g., "indoor", "corridor"
    confidence: float
    timestamp: float

@dataclass
class EntityUpdated:
    entity_id: str
    velocity: List[float] # [vx, vy, vz]
    visibility: float
    timestamp: float

@dataclass
class SpatialRelationshipUpdated:
    subject_id: str
    predicate: str # e.g., "next_to", "approaching"
    object_id: str
    timestamp: float
