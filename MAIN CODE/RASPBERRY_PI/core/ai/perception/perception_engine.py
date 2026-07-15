import asyncio
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

class PerceptionEngine:
    def __init__(self, analyzer: Any, stats: Any, publish: Callable):
        self.analyzer = analyzer
        self.stats = stats
        self.publish = publish
        
    async def execute(self, detections: list, depth_map: Any, robot_pose: dict):
        entities, scene, env_data, latency = await self.analyzer.analyze(detections, depth_map, robot_pose)
        
        # Update Stats
        self.stats.scenes_analyzed += 1
        self.stats.entities_tracked = len(entities)
        self.stats.avg_processing_latency_ms = (self.stats.avg_processing_latency_ms * 0.9) + (latency * 0.1)
        
        # Emit Semantic Object Events
        for e in entities:
            if e.get("visibility", 0) > 0.5: # only publish visible
                evt = {
                    "_perception_event_type": "SemanticObjectDetected",
                    "entity_id": str(e.get("tracking_id", "")),
                    "class_name": e.get("class_name", "unknown"),
                    "confidence": e.get("confidence", 0.0),
                    "world_coords": e.get("world_coords", [0,0,0]),
                    "distance_m": e.get("distance_m", -1.0),
                    "timestamp": asyncio.get_event_loop().time()
                }
                self.publish("perception.objects", evt)
                self.stats.events_published += 1
                
        # Emit Scene Event
        scene_evt = {
            "_perception_event_type": "SceneUpdated",
            "scene_id": f"scene_{self.stats.scenes_analyzed}",
            "entities": scene["entities"],
            "relationships": scene["relationships"],
            "timestamp": asyncio.get_event_loop().time()
        }
        self.publish("perception.scene", scene_evt)
        self.stats.events_published += 1
