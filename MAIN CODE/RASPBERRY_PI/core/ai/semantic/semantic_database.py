from typing import List, Dict, Any
from .persistent_storage import PersistentStorage

class SemanticDatabase:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        
    def insert_landmark(self, l_id: str, name: str, x: float, y: float, z: float):
        self.storage.execute(
            "INSERT OR REPLACE INTO landmarks (id, name, x, y, z) VALUES (?, ?, ?, ?, ?)",
            (l_id, name, x, y, z)
        )
        
    def insert_object(self, o_id: str, cls_name: str, x: float, y: float, z: float):
        self.storage.execute(
            "INSERT OR REPLACE INTO objects (id, class_name, x, y, z) VALUES (?, ?, ?, ?, ?)",
            (o_id, cls_name, x, y, z)
        )
