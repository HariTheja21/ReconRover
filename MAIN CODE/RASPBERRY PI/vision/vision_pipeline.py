"""
vision_pipeline.py
Recon Rover V1 - Vision Pipeline

Orchestrator for the asynchronous vision layer (Phase 4.3).
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, FrameCaptured, FrameProcessed, ObjectsDetected, SceneUpdated, VisionHealthUpdated
)

from .camera_manager import CameraManager
from .frame_buffer import FrameBuffer
from .frame_provider import FrameProvider
from .frame_preprocessor import FramePreprocessor
from .image_quality_monitor import ImageQualityMonitor
from .object_detector import ObjectDetector, MockDetector
from .object_classifier import MockClassifier
from .object_tracker import SimpleTracker
from .depth_estimator import MockDepthEstimator
from .landmark_detector import MockLandmarkDetector
from .scene_analyzer import SceneAnalyzer
from .vision_health import VisionHealth
from .vision_statistics import VisionStatistics

class VisionPipeline(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        
        self.health = VisionHealth()
        self.stats = VisionStatistics()
        
        self.camera = CameraManager(camera_id=0, fps=30)
        self.buffer = FrameBuffer(self.health, self.stats, maxsize=5)
        
        self.provider = FrameProvider(self.camera, self.buffer, self.event_bus, self.health, self.stats)
        self.iqm = ImageQualityMonitor()
        self.preprocessor = FramePreprocessor(self.health)
        
        self.detector = ObjectDetector(MockDetector(), self.health, self.stats)
        self.classifier = MockClassifier()
        self.tracker = SimpleTracker(max_missing_time=1.0)
        self.depth_est = MockDepthEstimator()
        self.landmark = MockLandmarkDetector()
        
        self.analyzer = SceneAnalyzer(self.event_bus)
        
        self._running = False
        self._task = None

    async def initialize(self):
        self.log.info("VisionPipeline (Phase 4.3) initialized.")

    async def start(self):
        self._running = True
        self.provider.start()
        self._task = asyncio.create_task(self._pipeline_loop())
        self.log.info("VisionPipeline started.")

    async def stop(self):
        self._running = False
        self.provider.stop()
        if self._task:
            self._task.cancel()
        self.log.info("VisionPipeline stopped.")

    def health(self) -> str:
        if self.health.camera_status != "CONNECTED":
            return "DEGRADED_CAMERA_DISCONNECTED"
        return "OK"

    async def _pipeline_loop(self):
        """Pulls frames from buffer, preprocesses, infers, tracks, and analyzes."""
        while self._running:
            try:
                # 1. Get raw frame from bounded buffer
                raw_data = await self.buffer.get()
                self.event_bus.publish(FrameCaptured(timestamp=raw_data["timestamp"]))
                
                # 2. Quality Check
                if not await self.iqm.analyze(raw_data):
                    self.buffer.task_done()
                    continue
                
                # 3. Preprocess
                processed_data = await self.preprocessor.process(raw_data)
                self.event_bus.publish(FrameProcessed(timestamp=raw_data["timestamp"]))
                self.stats.record_processed()
                
                # 4. Object Detection
                base_detections = await self.detector.run_detection(processed_data)
                
                # 5. Object Classification
                classified_detections = await self.classifier.run_classification(processed_data, base_detections)
                
                # 6. Object Tracking
                tracked_objects = await self.tracker.run_tracking(classified_detections, raw_data["timestamp"])
                
                # 7. Depth Estimation
                depth_objects = await self.depth_est.run_estimation(processed_data, tracked_objects)
                self.event_bus.publish(ObjectsDetected(objects=depth_objects))
                
                # 8. Landmark Extraction
                landmarks = await self.landmark.run_extraction(processed_data)
                
                # 9. Scene Analysis (Semantic Mapping)
                self.analyzer.analyze(depth_objects) # Scene analyzer publishes SceneUpdated internally
                
                self.buffer.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Pipeline loop error: {e}")
                await asyncio.sleep(0.5)
