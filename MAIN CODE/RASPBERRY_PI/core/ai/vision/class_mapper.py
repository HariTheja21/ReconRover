from typing import Dict

class ClassMapper:
    def __init__(self):
        # COCO mapping stub
        self.class_map: Dict[int, str] = {
            0: "person",
            39: "bottle",
            56: "chair",
            60: "table",
            62: "monitor",
            63: "laptop",
            64: "mouse",
            66: "keyboard",
            # add more as needed
        }
        
    def get_class_name(self, class_id: int) -> str:
        return self.class_map.get(class_id, f"unknown_{class_id}")
