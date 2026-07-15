import asyncio
from typing import Any
from .vision_health import VisionHealth
from .vision_statistics import VisionStatistics
from .vision_bridge import VisionBridge
from .model_loader import ModelLoader
from .frame_preprocessor import FramePreprocessor
from .frame_postprocessor import FramePostprocessor
from .object_detector import ObjectDetector
from .object_tracker import ObjectTracker
from .confidence_filter import ConfidenceFilter
from .detection_filter import DetectionFilter
from .class_mapper import ClassMapper
from .bounding_box_manager import BoundingBoxManager
from .vision_overlay import VisionOverlay
from .vision_pipeline import VisionPipeline
from .inference_worker import InferenceWorker
from .vision_scheduler import VisionScheduler

class VisionManager:
    def __init__(self, event_bus: Any):
        self.health = VisionHealth()
        self.stats = VisionStatistics()
        self.bridge = VisionBridge(event_bus)
        
        # Subcomponents
        self.loader = ModelLoader()
        self.preprocessor = FramePreprocessor()
        self.postprocessor = FramePostprocessor()
        
        # Core Pipeline Components
        self.detector = ObjectDetector(self.loader, self.preprocessor, self.postprocessor)
        self.tracker = ObjectTracker()
        self.conf_filter = ConfidenceFilter(threshold=0.5)
        self.det_filter = DetectionFilter()
        self.mapper = ClassMapper()
        self.bbox_manager = BoundingBoxManager()
        self.overlay = VisionOverlay()
        
        # Pipeline Assembly
        self.pipeline = VisionPipeline(
            self.detector, self.tracker, self.conf_filter, 
            self.det_filter, self.mapper, self.bbox_manager, self.overlay
        )
        
        # Workers & Scheduling
        self.worker = InferenceWorker(self.pipeline, self.stats, self.bridge.publish_event)
        self.scheduler = VisionScheduler(self.worker)
        
    async def start(self):
        # Start async worker loop
        asyncio.create_task(self.scheduler.run_loop())
