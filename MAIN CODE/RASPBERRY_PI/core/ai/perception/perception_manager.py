import asyncio
from typing import Any
from .perception_health import PerceptionHealth
from .perception_statistics import PerceptionStatistics
from .perception_bridge import PerceptionBridge
from .depth_estimator import DepthEstimator
from .distance_estimator import DistanceEstimator
from .object_correlator import ObjectCorrelator
from .world_projection import WorldProjection
from .confidence_fusion import ConfidenceFusion
from .entity_tracker import EntityTracker
from .visibility_manager import VisibilityManager
from .semantic_filter import SemanticFilter
from .spatial_reasoner import SpatialReasoner
from .scene_graph import SceneGraph
from .environment_classifier import EnvironmentClassifier
from .scene_analyzer import SceneAnalyzer
from .perception_engine import PerceptionEngine
from .perception_scheduler import PerceptionScheduler

class PerceptionManager:
    def __init__(self, event_bus: Any):
        self.health = PerceptionHealth()
        self.stats = PerceptionStatistics()
        self.bridge = PerceptionBridge(event_bus)
        
        # Subcomponents
        self.depth_est = DepthEstimator()
        self.dist_est = DistanceEstimator()
        self.correlator = ObjectCorrelator(self.depth_est, self.dist_est)
        self.proj = WorldProjection()
        self.fusion = ConfidenceFusion()
        self.tracker = EntityTracker()
        self.vis = VisibilityManager(self.tracker)
        self.sf = SemanticFilter()
        self.sr = SpatialReasoner()
        self.graph = SceneGraph()
        self.env = EnvironmentClassifier()
        
        # Assembly
        self.analyzer = SceneAnalyzer(
            self.correlator, self.proj, self.fusion, self.tracker, 
            self.vis, self.sf, self.sr, self.graph, self.env
        )
        
        # Engine & Scheduling
        self.engine = PerceptionEngine(self.analyzer, self.stats, self.bridge.publish_event)
        self.scheduler = PerceptionScheduler(self.engine)
        
    async def start(self):
        # Start async worker loop
        asyncio.create_task(self.scheduler.run_loop())
