from typing import List, Dict, Any

class WorldProjection:
    def __init__(self):
        # Camera intrinsics and extrinsics (stub)
        self.focal_length = 800.0 
        self.cx = 320.0
        self.cy = 240.0
        
    def project(self, detections: List[Dict[str, Any]], robot_pose: Dict[str, float]) -> List[Dict[str, Any]]:
        # Project 2D bounding box + distance + robot pose into 3D world coordinates
        for det in detections:
            dist = det.get("distance_m", -1.0)
            if dist > 0:
                # Stub mapping, assume straight ahead
                rx = robot_pose.get("x", 0.0)
                ry = robot_pose.get("y", 0.0)
                # Mock world coords
                det["world_coords"] = [rx + dist, ry, 0.0]
            else:
                det["world_coords"] = [0.0, 0.0, 0.0]
        return detections
