import asyncio
from typing import Any

from .vision_health import VisionHealth
from .vision_statistics import VisionStatistics
from .vision_bridge import VisionBridge
from .vision_preprocessor import VisionPreprocessor
from .vision_postprocessor import VisionPostprocessor
from .vision_registry import VisionRegistry
from .vision_loader import VisionLoader
from .vision_inference import VisionInference
from .vision_scheduler import VisionScheduler

from .models.yolo_provider import YOLOProvider
from .models.rtdetr_provider import RTDETRProvider
from .models.fastsam_provider import FastSAMProvider
from .models.depth_anything_provider import DepthAnythingProvider

class VisionRuntime:
    def __init__(self, event_bus: Any):
        self.health = VisionHealth()
        self.stats = VisionStatistics()
        self.bridge = VisionBridge(event_bus)
        
        self.registry = VisionRegistry()
        self._register_default_models()
        
        self.loader = VisionLoader(self.registry)
        self.preprocessor = VisionPreprocessor()
        self.postprocessor = VisionPostprocessor()
        
        self.inference = VisionInference(self.loader, self.preprocessor, self.postprocessor)
        self.scheduler = VisionScheduler(self.inference, self.bridge)
        
    def _register_default_models(self):
        self.registry.register("yolo11", YOLOProvider)
        self.registry.register("rt-detr", RTDETRProvider)
        self.registry.register("fastsam", FastSAMProvider)
        self.registry.register("depth_anything", DepthAnythingProvider)
        
    async def initialize(self):
        # Stub init
        return True
