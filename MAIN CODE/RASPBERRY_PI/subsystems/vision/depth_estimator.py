"""
depth_estimator.py
Recon Rover V1 - Vision Pipeline

Abstract interface for monocular or stereo depth estimation.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

class DepthEstimator(ABC):
    @abstractmethod
    def estimate_depth(self, frame_data: Any, detections: List[Dict]) -> List[Dict]:
        """
        Appends depth/distance information to tracked detections.
        """
        raise NotImplementedError("Subclasses must implement estimate_depth")

class MockDepthEstimator(DepthEstimator):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="DepthEst")

    async def run_estimation(self, frame_data: Any, detections: List[Dict]) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.estimate_depth, frame_data, detections)

    def estimate_depth(self, frame_data: Any, detections: List[Dict]) -> List[Dict]:
        import time
        time.sleep(0.002)
        
        results = []
        for det in detections:
            det_copy = det.copy()
            # Fake a distance in meters
            det_copy["distance_m"] = 1.5 
            results.append(det_copy)
        return results
