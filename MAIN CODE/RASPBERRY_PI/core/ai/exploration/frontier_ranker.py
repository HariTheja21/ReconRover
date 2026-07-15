from typing import List, Dict, Any
import math

class FrontierRanker:
    def __init__(self):
        pass
        
    def rank(self, clusters: List[Dict[str, Any]], robot_pose: tuple) -> List[Dict[str, Any]]:
        # Stub: rank clusters by distance, size, and information gain
        rx, ry = robot_pose
        for cluster in clusters:
            cx, cy = cluster["centroid"]
            dist = math.hypot(cx - rx, cy - ry)
            cluster["score"] = cluster["size"] / (dist + 1.0)
            
        return sorted(clusters, key=lambda c: c["score"], reverse=True)
