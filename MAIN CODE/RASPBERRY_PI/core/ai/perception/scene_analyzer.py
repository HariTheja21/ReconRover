import asyncio
import time
from typing import List, Dict, Any
from .object_correlator import ObjectCorrelator
from .world_projection import WorldProjection
from .confidence_fusion import ConfidenceFusion
from .entity_tracker import EntityTracker
from .visibility_manager import VisibilityManager
from .semantic_filter import SemanticFilter
from .spatial_reasoner import SpatialReasoner
from .scene_graph import SceneGraph
from .environment_classifier import EnvironmentClassifier

class SceneAnalyzer:
    def __init__(self, correlator: ObjectCorrelator, proj: WorldProjection, fusion: ConfidenceFusion,
                 tracker: EntityTracker, vis: VisibilityManager, sf: SemanticFilter, 
                 sr: SpatialReasoner, graph: SceneGraph, env: EnvironmentClassifier):
        self.correlator = correlator
        self.proj = proj
        self.fusion = fusion
        self.tracker = tracker
        self.vis = vis
        self.sf = sf
        self.sr = sr
        self.graph = graph
        self.env = env
        
    async def analyze(self, detections: List[Dict[str, Any]], depth_map: Any, robot_pose: Dict[str, float]) -> tuple[List[Dict[str, Any]], Dict[str, Any], tuple[str, float], float]:
        start_time = time.time()
        
        # 1. Correlate with depth
        entities = self.correlator.correlate(detections, depth_map)
        
        # 2. Project to World Coordinates
        entities = self.proj.project(entities, robot_pose)
        
        # 3. Fuse confidence (mock sensor conf = 1.0)
        for e in entities:
            e["confidence"] = self.fusion.fuse(e.get("confidence", 0.5), 1.0)
            
        # 4. Semantic Filtering
        entities = self.sf.filter_noise(entities)
        
        # 5. Track and maintain object permanence
        self.tracker.update(entities)
        current_ids = {str(e.get("tracking_id")) for e in entities}
        self.vis.decay_visibility(current_ids)
        
        # Get active entities
        active_entities = list(self.tracker.entities.values())
        
        # 6. Spatial Reasoning
        relationships = self.sr.infer_relationships(active_entities)
        
        # 7. Update Scene Graph
        self.graph.update(active_entities, relationships)
        
        # 8. Environment Classification
        env_class, env_conf = self.env.classify(self.graph, None) # SLAM grid stub
        
        latency = (time.time() - start_time) * 1000
        return active_entities, self.graph.get_snapshot(), (env_class, env_conf), latency
