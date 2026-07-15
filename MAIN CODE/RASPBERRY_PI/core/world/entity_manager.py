"""
Entity Manager Module
Recon Rover V2 - Phase 3.1
"""
import threading
from .entity import Entity

class EntityManager:
    """Tracks dynamic entities identified in the environment."""
    def __init__(self):
        self._lock = threading.RLock()
        self.entities = {}
        
    def add_or_update(self, entity_id: str, semantic_class: str, confidence: float):
        with self._lock:
            if entity_id in self.entities:
                self.entities[entity_id].confidence = confidence
                self.entities[entity_id].update_timestamp()
            else:
                self.entities[entity_id] = Entity(entity_id, semantic_class, confidence)
                
    def get_all(self):
        with self._lock:
            return list(self.entities.values())
