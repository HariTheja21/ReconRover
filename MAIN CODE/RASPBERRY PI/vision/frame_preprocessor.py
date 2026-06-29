"""
frame_preprocessor.py
Recon Rover V1 - Vision Pipeline

Asynchronously resizes, normalizes, and crops frames in a thread pool.
Replaces legacy image_processor.py.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from logger import Logger
from .vision_health import VisionHealth

class FramePreprocessor:
    def __init__(self, health: VisionHealth):
        self.health = health
        self.log = Logger.get("FramePreprocessor")
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="Preproc")

    async def process(self, raw_data: dict) -> dict:
        """
        Takes raw frame dict (frame + timestamp) and returns a processed version.
        Runs heavy CPU operations in the executor.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self._process_sync, raw_data)

    def _process_sync(self, raw_data: dict) -> dict:
        # Mocking actual OpenCV operations to avoid blocking or memory issues
        # In a real implementation: cv2.resize, cv2.cvtColor, etc.
        frame = raw_data["frame"]
        
        # Simulate processing time
        import time
        time.sleep(0.005)
        
        return {
            "processed_frame": f"processed_{frame}",
            "original_frame": frame,
            "timestamp": raw_data["timestamp"]
        }
