import uuid
from typing import Any

class LandmarkManager:
    def __init__(self, db: Any):
        self.db = db
        
    def create_landmark(self, name: str, x: float, y: float, z: float) -> str:
        l_id = str(uuid.uuid4())
        self.db.insert_landmark(l_id, name, x, y, z)
        return l_id
