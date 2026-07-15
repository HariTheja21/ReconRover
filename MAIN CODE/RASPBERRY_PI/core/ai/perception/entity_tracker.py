from typing import Dict, Any, List

class EntityTracker:
    def __init__(self):
        # Persistent memory of entities in the world (Object Permanence)
        self.entities: Dict[str, Dict[str, Any]] = {}
        
    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Update entity states, handle occlusions, calculate velocities
        current_ids = set()
        for det in detections:
            tid = str(det.get("tracking_id", "unknown"))
            current_ids.add(tid)
            if tid not in self.entities:
                self.entities[tid] = {"first_seen": det.get("timestamp", 0.0)}
            
            # Update position and properties
            self.entities[tid].update(det)
            self.entities[tid]["visibility"] = 1.0 # visible
            
        return detections
