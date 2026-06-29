"""
audio_provider.py
Recon Rover V1 - Audio Pipeline

Asynchronously pulls audio chunks from the microphone manager and places them in the bounded buffer.
Replaces the legacy audio_capture.py.
"""

import asyncio
import time
from logger import Logger
from event_bus import EventBus
from .microphone_manager import MicrophoneManager
from .audio_buffer import AudioBuffer
from .audio_health import AudioHealth
from .audio_statistics import AudioStatistics

class AudioProvider:
    def __init__(self, mic: MicrophoneManager, buffer: AudioBuffer, event_bus: EventBus, health: AudioHealth, stats: AudioStatistics):
        self.mic = mic
        self.buffer = buffer
        self.event_bus = event_bus
        self.health = health
        self.stats = stats
        self.log = Logger.get("AudioProvider")
        
        self._running = False
        self._task = None

    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._capture_loop())
        self.log.info("AudioProvider started.")

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("AudioProvider stopped.")

    async def _capture_loop(self):
        while self._running:
            try:
                chunk = await self.mic.read_chunk()
                if chunk is not None:
                    timestamp = time.perf_counter()
                    # Non-blocking put with eviction of oldest if full
                    self.buffer.put_nowait({"chunk": chunk, "timestamp": timestamp})
                    self.stats.record_captured()
                    
                # Yield to event loop, maintaining rough sampling constraint
                # (Assuming roughly 10 chunks per second in legacy setup)
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"AudioProvider loop error: {e}")
                self.health.mic_status = "ERROR"
                await asyncio.sleep(1.0)
