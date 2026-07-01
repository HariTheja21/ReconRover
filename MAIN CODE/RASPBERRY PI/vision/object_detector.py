"""
object_detector.py
Recon Rover V1 - Vision Pipeline

Abstract detector interface and a lightweight mock implementation.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import asyncio
import time
from logger import Logger
from .vision_health import VisionHealth
from .vision_statistics import VisionStatistics

class ObjectDetectorInterface(ABC):
    @abstractmethod
    def detect(self, frame: bytes) -> List[Dict]:
        """Returns a list of dicts with 'class', 'confidence', 'bbox'."""
        raise NotImplementedError("Subclasses must implement detect")

class MockDetector(ObjectDetectorInterface):
    """
    Placeholder detector to support the pipeline without a heavy model.
    """
    def detect(self, frame: bytes) -> List[Dict]:
        time.sleep(0.02) # Simulate 20ms inference
        # Mock detection: returns a person every time for testing architecture
        return [
            {"class": "person", "confidence": 0.95, "bbox": [10, 10, 100, 100]}
        ]

class ObjectDetector:
    def __init__(self, backend: ObjectDetectorInterface, health: VisionHealth, stats: VisionStatistics):
        self.backend = backend
        self.health = health
        self.stats = stats
        self.log = Logger.get("ObjectDetector")
        self.loop = asyncio.get_running_loop()

    async def run_detection(self, frame: bytes) -> List[Dict]:
        start = time.perf_counter()
        
        detections = await self.loop.run_in_executor(None, self.backend.detect, frame)
        
        latency = (time.perf_counter() - start) * 1000
        self.health.detection_latency_ms = latency
        self.stats.record_detection(len(detections))
        
        return detections
