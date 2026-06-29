"""
sound_classifier.py
Recon Rover V1 - Audio Pipeline

Abstract interface for general environmental sound classification.
"""

from abc import ABC, abstractmethod
from typing import Any, List
import asyncio
from concurrent.futures import ThreadPoolExecutor

class SoundClassifier(ABC):
    @abstractmethod
    def classify(self, processed_chunk: Any) -> List[str]:
        """
        Returns a list of classified sounds.
        Supported tags: 'Human voice', 'Vehicle', 'Animal', 'Alarm', 'Explosion', 'Wind', 'Rain', 'Unknown'
        """
        pass

class MockSoundClassifier(SoundClassifier):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="SndClass")

    async def run_classification(self, processed_chunk: Any) -> List[str]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.classify, processed_chunk)

    def classify(self, processed_chunk: Any) -> List[str]:
        import time
        time.sleep(0.002)
        # Mock logic
        return ["Unknown"]
