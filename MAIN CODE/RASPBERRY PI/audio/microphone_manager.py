"""
microphone_manager.py
Recon Rover V1 - Audio Pipeline

Manages the USB microphone connection lifecycle and auto-reconnect logic.
"""

import asyncio
from logger import Logger
import time

class MicrophoneManager:
    """
    Mock implementation for now, meant to wrap PyAudio or SoundDevice.
    Manages the microphone handle and reconnect logic.
    """
    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.is_connected = False
        self.log = Logger.get("MicrophoneManager")
        self._reconnect_delay = 1.0

    def connect(self) -> bool:
        """Attempts to open the microphone."""
        # Mock connection success
        self.is_connected = True
        self.log.info("USB Microphone connected.")
        return True

    def disconnect(self):
        """Closes the microphone."""
        self.is_connected = False
        self.log.info("USB Microphone disconnected.")

    async def wait_before_reconnect(self):
        """Exponential backoff for microphone reconnects."""
        await asyncio.sleep(self._reconnect_delay)
        self._reconnect_delay = min(self._reconnect_delay * 1.5, 10.0)

    def reset_backoff(self):
        self._reconnect_delay = 1.0

    def get_chunk(self) -> bytes:
        """
        Mocks reading a chunk of audio from the microphone.
        In reality, this would be stream.read(chunk_size).
        Returns dummy bytes.
        """
        if not self.is_connected:
            return b""
        
        # Simulate blocking read based on chunk size and sample rate
        delay = self.chunk_size / self.sample_rate
        time.sleep(delay) 
        
        # Return a mock chunk
        return b"MOCK_AUDIO_CHUNK"
