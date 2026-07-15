from typing import List, Dict, Any

class ConfidenceFilter:
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        
    def filter(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [d for d in detections if d.get("confidence", 0.0) >= self.threshold]
