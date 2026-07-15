from typing import List, Dict, Any
from .depth_estimator import DepthEstimator
from .distance_estimator import DistanceEstimator

class ObjectCorrelator:
    def __init__(self, depth: DepthEstimator, dist: DistanceEstimator):
        self.depth = depth
        self.dist = dist
        
    def correlate(self, detections: List[Dict[str, Any]], depth_map: Any) -> List[Dict[str, Any]]:
        # Correlate 2D bounding boxes with depth/distance data
        for det in detections:
            bbox = det.get("bbox", [0,0,0,0])
            distance = self.dist.estimate_distance(bbox, depth_map)
            det["distance_m"] = distance
        return detections
