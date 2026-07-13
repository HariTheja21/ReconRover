"""
vl_scene_builder.py
Recon Rover V1 - Vision-Language Cognitive Integration

Converts semantic Vision detections into the structured VLSceneGraph.
"""

from typing import List, Dict, Any
from .vl_scene_graph import VLSceneGraph

class VLSceneBuilder:
    def __init__(self, scene_graph: VLSceneGraph):
        self.graph = scene_graph

    def build_from_detections(self, detections: List[Dict[str, Any]]):
        """
        Rebuilds the graph purely from semantic dictionaries.
        No OpenCV or image processing required.
        """
        self.graph.clear()
        
        for i, det in enumerate(detections):
            # Create a unique node ID
            node_id = f"{det.get('class', 'unknown')}_{i}"
            
            # Extract relevant attributes
            attributes = {
                "class": det.get("class", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "distance": det.get("distance", -1.0)
            }
            
            # Incorporate spatial bounding box centers if provided
            bbox = det.get("bbox", [])
            if len(bbox) == 4:
                # [x1, y1, x2, y2]
                attributes["cx"] = (bbox[0] + bbox[2]) / 2.0
                attributes["cy"] = (bbox[1] + bbox[3]) / 2.0
                
            self.graph.add_node(node_id, attributes)
            
        # Compute automatic edges
        self.graph.compute_spatial_relations()
