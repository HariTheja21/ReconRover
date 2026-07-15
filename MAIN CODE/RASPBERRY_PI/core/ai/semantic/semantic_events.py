from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class LandmarkCreated:
    landmark_id: str
    name: str
    x: float
    y: float
    z: float
    timestamp: float

@dataclass
class SemanticMapUpdated:
    new_entities: int
    total_entities: int
    timestamp: float

@dataclass
class RoomClassified:
    room_id: str
    classification: str
    confidence: float
    timestamp: float

@dataclass
class KnowledgeGraphUpdated:
    nodes_added: int
    edges_added: int
    timestamp: float

@dataclass
class SemanticMemoryUpdated:
    memory_type: str
    status: str
    timestamp: float
