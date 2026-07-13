"""
vl_memory_bridge.py
Recon Rover V1 - Vision-Language Cognitive Integration

Identifies major scene shifts to trigger episodic memories.
"""

from event_bus import EventBus, SceneSummaryUpdated
from .vl_scene_graph import VLSceneGraph

class VLMemoryBridge:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.last_scene_hash = ""

    def evaluate_and_publish(self, caption: str, graph: VLSceneGraph):
        """
        Determines if the scene has changed enough to warrant a memory.
        """
        # Simple hash based on object classes in scene
        classes = sorted([attrs.get("class", "unk") for attrs in graph.nodes.values()])
        current_hash = "_".join(classes)
        
        # Only publish if the semantic structure fundamentally changed
        # (e.g., a person entered, or an obstacle cleared)
        if current_hash != self.last_scene_hash:
            self.last_scene_hash = current_hash
            
            self.event_bus.publish(SceneSummaryUpdated(
                summary=caption
            ))
