"""
vl_observation_generator.py
Recon Rover V1 - Vision-Language Cognitive Integration

Generates high-density, token-efficient observations for LLM context.
"""

from .vl_scene_graph import VLSceneGraph

class VLObservationGenerator:
    def generate_observation(self, graph: VLSceneGraph) -> str:
        """
        Creates a compressed string optimized for LLM token usage.
        Format: [VISION] Person(dist=2.1, conf=0.9) | Chair(dist=1.5) => Chair NEAR Person
        """
        if not graph.nodes:
            return "[VISION] Empty"
            
        obs_parts = []
        
        # Objects
        obj_strings = []
        for node_id, attrs in graph.nodes.items():
            cls = attrs.get("class", "obj")
            dist = attrs.get("distance", -1.0)
            conf = attrs.get("confidence", 0.0)
            
            dist_str = f"d={dist:.1f}m" if dist >= 0 else "d=unk"
            obj_strings.append(f"{cls.capitalize()}({dist_str},c={conf:.2f})")
            
        obs_parts.append(", ".join(obj_strings))
        
        # Relations
        rel_strings = []
        for edge in graph.edges:
            src_id, tgt_id, relation = edge
            src_cls = graph.nodes[src_id].get("class", "obj").capitalize()
            tgt_cls = graph.nodes[tgt_id].get("class", "obj").capitalize()
            rel_strings.append(f"{src_cls}_{relation}_{tgt_cls}")
            
        if rel_strings:
            obs_parts.append("| " + ", ".join(rel_strings))
            
        return "[VISION] " + " ".join(obs_parts)
