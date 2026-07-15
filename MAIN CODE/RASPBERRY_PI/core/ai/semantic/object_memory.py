from typing import Any

class ObjectMemory:
    def __init__(self, db: Any):
        self.db = db
        self.in_memory_cache = {}
        
    def update_object(self, o_id: str, cls_name: str, x: float, y: float, z: float):
        self.in_memory_cache[o_id] = {"class": cls_name, "x": x, "y": y, "z": z}
        self.db.insert_object(o_id, cls_name, x, y, z)
