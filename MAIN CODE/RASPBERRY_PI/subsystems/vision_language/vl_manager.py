"""
vl_manager.py
Recon Rover V1 - Vision-Language Cognitive Integration

Coordinates the internal VL pipeline from detection to LLM context.
"""

from typing import List, Dict, Any
from event_bus import EventBus
from .vl_context import VLContext
from .vl_scene_graph import VLSceneGraph
from .vl_scene_builder import VLSceneBuilder
from .vl_caption_generator import VLCaptionGenerator
from .vl_observation_generator import VLObservationGenerator
from .vl_reasoning_bridge import VLReasoningBridge
from .vl_memory_bridge import VLMemoryBridge
from .vl_health import VLHealth
from .vl_statistics import VLStatistics

class VLManager:
    def __init__(self, event_bus: EventBus):
        self.context = VLContext()
        self.graph = VLSceneGraph()
        
        self.builder = VLSceneBuilder(self.graph)
        self.caption_gen = VLCaptionGenerator()
        self.obs_gen = VLObservationGenerator()
        
        self.reasoning = VLReasoningBridge(event_bus)
        self.memory = VLMemoryBridge(event_bus)
        
        self.health = VLHealth()
        self.stats = VLStatistics()

    def process_detections(self, detections: List[Dict[str, Any]]):
        """Runs the pipeline on new semantic detections."""
        try:
            # 1. Update State
            self.context.latest_detections = detections
            
            # 2. Build Spatial Graph
            self.builder.build_from_detections(detections)
            self.stats.record_graph()
            
            # 3. Generate Representations
            caption = self.caption_gen.generate_caption(self.graph)
            observation = self.obs_gen.generate_observation(self.graph)
            
            # 4. Bridge to LLM
            self.reasoning.publish_observation(observation)
            self.stats.record_observation()
            
            # 5. Bridge to Memory
            self.memory.evaluate_and_publish(caption, self.graph)
            self.stats.record_memory()
            
            self.health.record_success()
        except Exception:
            self.health.record_error()
