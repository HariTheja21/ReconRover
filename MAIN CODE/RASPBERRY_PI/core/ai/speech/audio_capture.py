import asyncio
from typing import Callable, Any

class AudioCapture:
    def __init__(self):
        self.is_recording = False
        self.callback = None
        
    def set_callback(self, cb: Callable):
        self.callback = cb
        
    async def start_stream(self):
        self.is_recording = True
        # Stub: loop reading from microphone using PyAudio/SoundDevice
        pass
        
    def stop_stream(self):
        self.is_recording = False
        
    def mock_inject_audio(self, audio_data: bytes):
        if self.callback:
            self.callback(audio_data)
