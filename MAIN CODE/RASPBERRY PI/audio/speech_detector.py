"""
speech_detector.py
Recon Rover V1 - Audio Pipeline

Abstract interface for detecting and segmenting speech utterances.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

class SpeechDetector(ABC):
    @abstractmethod
    def detect_speech(self, processed_chunk: Any, vad_active: bool) -> Optional[Any]:
        """
        Takes raw audio and a VAD flag. If speech is ongoing, buffers it.
        Returns a complete utterance segment when speech stops, otherwise None.
        """
        pass

class MockSpeechDetector(SpeechDetector):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="SpeechDet")
        self.is_speaking = False

    async def run_detection(self, processed_chunk: Any, vad_active: bool) -> Optional[Any]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.detect_speech, processed_chunk, vad_active)

    def detect_speech(self, processed_chunk: Any, vad_active: bool) -> Optional[Any]:
        import time
        time.sleep(0.001)
        # Mock logic
        return None
