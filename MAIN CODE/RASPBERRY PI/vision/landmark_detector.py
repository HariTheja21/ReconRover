"""
landmark_detector.py
Recon Rover V1 - Vision Pipeline

Extracts static environmental landmarks for mapping and localization.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

class LandmarkDetector(ABC):
    @abstractmethod
    def extract_landmarks(self, frame_data: Any) -> List[Dict]:
        """
        Extracts keypoints, ORB/SIFT features, or structural markers (doors, signs).
        """
        raise NotImplementedError("Subclasses must implement extract_landmarks")

class MockLandmarkDetector(LandmarkDetector):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="Landmark")

    async def run_extraction(self, frame_data: Any) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.extract_landmarks, frame_data)

    def extract_landmarks(self, frame_data: Any) -> List[Dict]:
        import time
        time.sleep(0.001)
        
        # Mock returning a list of generic structural landmarks
        return [
            {"type": "corner", "x": 100, "y": 200, "descriptor": [0.1, 0.2]}
        ]
