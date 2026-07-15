"""
Entity Module
Recon Rover V2 - Phase 3.1
"""
import time
from dataclasses import dataclass, field

@dataclass
class Entity:
    """Base class for any physical object in the world model."""
    entity_id: str
    semantic_class: str
    confidence: float
    timestamp: float = field(default_factory=time.time)
    
    def update_timestamp(self):
        self.timestamp = time.time()
