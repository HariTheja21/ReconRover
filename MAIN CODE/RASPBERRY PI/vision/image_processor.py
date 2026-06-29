"""
image_processor.py
Recon Rover V1 - Vision Pipeline

Handles resizing and normalization of frames.
"""

import asyncio
import time
from logger import Logger
from .vision_health import VisionHealth

class ImageProcessor:
    def __init__(self, health: VisionHealth):
        self.health = health
        self.log = Logger.get("ImageProcessor")
        self.loop = asyncio.get_running_loop()

    def _process(self, frame: bytes) -> bytes:
        """
        Mock image processing (resize/color conversion).
        In reality, this would use OpenCV.
        """
        # Simulate processing time
        time.sleep(0.01)
        return b"PROCESSED_FRAME_DATA"

    async def process_frame(self, frame: bytes) -> bytes:
        """
        Runs the blocking image processing in a thread pool.
        """
        start = time.perf_counter()
        
        processed = await self.loop.run_in_executor(None, self._process, frame)
        
        latency = (time.perf_counter() - start) * 1000
        self.health.processing_latency_ms = latency
        
        return processed
