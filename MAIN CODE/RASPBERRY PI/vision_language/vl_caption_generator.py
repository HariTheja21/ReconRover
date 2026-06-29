"""
vl_caption_generator.py
Recon Rover V1 - Vision-Language Cognitive Integration

Generates human-readable summaries of the scene graph.
"""

from .vl_scene_graph import VLSceneGraph

class VLCaptionGenerator:
    def generate_caption(self, graph: VLSceneGraph) -> str:
        """
        Creates a deterministic paragraph describing the scene.
        """
        if not graph.nodes:
            return "The scene is empty."
            
        sentences = []
        
        # Summarize objects
        objects_by_class = {}
        for node_id, attrs in graph.nodes.items():
            cls = attrs.get("class", "object")
            objects_by_class[cls] = objects_by_class.get(cls, 0) + 1
            
        obj_desc = []
        for cls, count in objects_by_class.items():
            if count == 1:
                obj_desc.append(f"a {cls}")
            else:
                obj_desc.append(f"{count} {cls}s")
                
        sentences.append(f"I see {', '.join(obj_desc)}.")
        
        # Summarize relations
        for edge in graph.edges:
            src_id, tgt_id, relation = edge
            src_cls = graph.nodes[src_id].get("class", "object")
            tgt_cls = graph.nodes[tgt_id].get("class", "object")
            
            if relation == "NEAR":
                sentences.append(f"A {src_cls} is near a {tgt_cls}.")
            elif relation == "BLOCKING":
                sentences.append(f"A {src_cls} is blocking the {tgt_cls}.")
                
        return " ".join(sentences)
