"""
direction_estimator.py
Recon Rover V1 - Audio Pipeline

Abstract interface for Direction of Arrival (DOA) estimation.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor

class DirectionEstimator(ABC):
    @abstractmethod
    def estimate(self, processed_chunk: Any) -> Optional[Dict[str, float]]:
        """
        Returns estimated direction in degrees (azimuth, elevation) if applicable.
        """
        raise NotImplementedError("Subclasses must implement estimate")

class MockDirectionEstimator(DirectionEstimator):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="DOA")

    async def run_estimation(self, processed_chunk: Any) -> Optional[Dict[str, float]]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.estimate, processed_chunk)

    def estimate(self, processed_chunk: Any) -> Optional[Dict[str, float]]:
        import time
        time.sleep(0.001)
        # Mock logic
        return {"azimuth": 0.0, "elevation": 0.0}
