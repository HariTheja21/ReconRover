"""
vl_scene_graph.py
Recon Rover V1 - Vision-Language Cognitive Integration

Maintains nodes (objects) and edges (spatial/logical relationships).
"""

from typing import List, Dict, Any, Tuple
import math

class VLSceneGraph:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Tuple[str, str, str]] = []  # (source_id, target_id, relation)

    def clear(self):
        self.nodes.clear()
        self.edges.clear()

    def add_node(self, node_id: str, attributes: Dict[str, Any]):
        self.nodes[node_id] = attributes

    def add_edge(self, source: str, target: str, relation: str):
        if source in self.nodes and target in self.nodes:
            self.edges.append((source, target, relation))

    def compute_spatial_relations(self, proximity_threshold: float = 1.5):
        """
        Calculates simple spatial relations based on distance attributes.
        Assumes nodes have 'x', 'y' or 'distance' attributes if available from world model.
        """
        node_ids = list(self.nodes.keys())
        for i in range(len(node_ids)):
            for j in range(i + 1, len(node_ids)):
                id1, id2 = node_ids[i], node_ids[j]
                n1, n2 = self.nodes[id1], self.nodes[id2]
                
                # If we have 3D space coords from world model
                if 'x' in n1 and 'y' in n1 and 'x' in n2 and 'y' in n2:
                    dist = math.hypot(n1['x'] - n2['x'], n1['y'] - n2['y'])
                    if dist < proximity_threshold:
                        self.add_edge(id1, id2, "NEAR")
                        self.add_edge(id2, id1, "NEAR")
                
                # Check for blockers
                if n1.get("class") == "obstacle" and n2.get("class") == "hallway":
                    self.add_edge(id1, id2, "BLOCKING")
