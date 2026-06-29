"""
sound_detector.py
Recon Rover V1 - Audio Pipeline

Abstract detector interface and a lightweight mock implementation.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import asyncio
import time
from logger import Logger
from .audio_health import AudioHealth
from .audio_statistics import AudioStatistics

class SoundDetectorInterface(ABC):
    @abstractmethod
    def detect(self, chunk: bytes) -> List[Dict]:
        """Returns a list of dicts with 'class' and 'confidence'."""
        pass

class MockSoundDetector(SoundDetectorInterface):
    """
    Placeholder detector to support the pipeline without a heavy model.
    """
    def detect(self, chunk: bytes) -> List[Dict]:
        time.sleep(0.015) # Simulate 15ms inference
        # Mock detection: returns human speech every time for testing architecture
        return [
            {"class": "human_speech", "confidence": 0.85}
        ]

class SoundDetector:
    def __init__(self, backend: SoundDetectorInterface, health: AudioHealth, stats: AudioStatistics):
        self.backend = backend
        self.health = health
        self.stats = stats
        self.log = Logger.get("SoundDetector")
        self.loop = asyncio.get_running_loop()

    async def run_detection(self, chunk: bytes) -> List[Dict]:
        start = time.perf_counter()
        
        detections = await self.loop.run_in_executor(None, self.backend.detect, chunk)
        
        latency = (time.perf_counter() - start) * 1000
        self.health.detection_latency_ms = latency
        self.stats.record_detection(len(detections))
        
        return detections
