from typing import List
import numpy as np

class DistanceEstimator:
    def __init__(self):
        pass
        
    def estimate_distance(self, bbox: List[int], depth_map: np.ndarray) -> float:
        # Given a bounding box [x, y, w, h] and a depth map, estimate distance to object
        # Stub: return median depth in bbox area
        x, y, w, h = bbox
        if depth_map is None or w == 0 or h == 0:
            return -1.0
            
        roi = depth_map[y:y+h, x:x+w]
        if roi.size == 0:
            return -1.0
            
        return float(np.median(roi))
