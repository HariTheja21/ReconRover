from typing import Dict, Any

class VisibilityManager:
    def __init__(self, tracker: Any):
        self.tracker = tracker
        
    def decay_visibility(self, current_ids: set, decay_rate: float = 0.1):
        # Reduce visibility of entities not seen in current frame
        keys_to_remove = []
        for tid, entity in self.tracker.entities.items():
            if tid not in current_ids:
                entity["visibility"] = max(0.0, entity.get("visibility", 1.0) - decay_rate)
                if entity["visibility"] <= 0:
                    keys_to_remove.append(tid)
                    
        for k in keys_to_remove:
            del self.tracker.entities[k]
