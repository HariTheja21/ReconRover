import asyncio
from typing import Any
from .speech_manager import SpeechManager

class SpeechRuntime:
    """
    Top-level facade for the Speech AI Engine.
    Handles configuration and API access for Voice interaction.
    """
    def __init__(self, event_bus: Any):
        self.manager = SpeechManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    async def request_speech(self, text: str, voice_profile: str = "default"):
        """Request the rover to speak text aloud"""
        await self.manager.scheduler.enqueue_tts(text, voice_profile)
        
    def inject_mock_audio(self, audio_bytes: bytes):
        """For testing without physical microphone"""
        self.manager.capture.mock_inject_audio(audio_bytes)
