from typing import List, Dict, Any

class DetectionFilter:
    def __init__(self):
        # Only allow these classes through the pipeline
        self.allowed_classes = set(["person", "chair", "bottle", "laptop", "backpack", "door", "table", "monitor", "keyboard", "mouse"])
        
    def set_allowed_classes(self, classes: List[str]):
        self.allowed_classes = set(classes)
        
    def filter(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [d for d in detections if d.get("class_name", "").lower() in self.allowed_classes]
