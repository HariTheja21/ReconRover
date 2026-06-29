"""
speech_recognizer.py
Recon Rover V1 - Audio Pipeline

Abstract interface for Speech-to-Text (STT) inference.
"""

from abc import ABC, abstractmethod
from typing import Any, str
import asyncio
from concurrent.futures import ThreadPoolExecutor

class SpeechRecognizer(ABC):
    @abstractmethod
    def transcribe(self, speech_segment: Any) -> str:
        """
        Converts an isolated speech segment into transcribed text.
        """
        pass

class MockSpeechRecognizer(SpeechRecognizer):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="STT")

    async def run_transcription(self, speech_segment: Any) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.transcribe, speech_segment)

    def transcribe(self, speech_segment: Any) -> str:
        import time
        time.sleep(0.01)
        return "mock transcription"
