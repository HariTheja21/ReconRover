import json
import os
import uuid
from typing import Dict, List, Optional

class MissionStorage:
    def __init__(self, storage_dir: str = "data/missions"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
            
    def _get_filepath(self, mission_id: str) -> str:
        return os.path.join(self.storage_dir, f"{mission_id}.json")

    def save_mission(self, mission_data: dict) -> str:
        mission_id = mission_data.get("id", str(uuid.uuid4()))
        mission_data["id"] = mission_id
        
        filepath = self._get_filepath(mission_id)
        with open(filepath, 'w') as f:
            json.dump(mission_data, f, indent=4)
        return mission_id

    def load_mission(self, mission_id: str) -> Optional[dict]:
        filepath = self._get_filepath(mission_id)
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r') as f:
            return json.load(f)

    def list_missions(self) -> List[dict]:
        missions = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.storage_dir, filename), 'r') as f:
                    data = json.load(f)
                    # Return summary data, not full waypoints if huge
                    missions.append({
                        "id": data.get("id"),
                        "name": data.get("name", "Unnamed"),
                        "type": data.get("type", "Waypoint"),
                        "waypoint_count": len(data.get("waypoints", []))
                    })
        return missions

    def delete_mission(self, mission_id: str) -> bool:
        filepath = self._get_filepath(mission_id)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
