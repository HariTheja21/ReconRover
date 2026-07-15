from typing import Dict, Any

class EnvironmentClassifier:
    def __init__(self):
        pass
        
    def classify(self, scene_graph: Any, occupancy_grid: Any) -> tuple[str, float]:
        # Classify the room type (e.g., "office", "corridor", "outdoor") based on 
        # objects present and SLAM geometry
        return "indoor_generic", 0.8
