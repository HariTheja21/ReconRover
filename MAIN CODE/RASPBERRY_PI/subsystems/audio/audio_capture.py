"""
audio_capture.py
Recon Rover V1 - Audio Pipeline

Asynchronously captures audio chunks from the MicrophoneManager.
"""

import asyncio
import time
from logger import Logger
from .microphone_manager import MicrophoneManager
from .audio_buffer import AudioBuffer
from event_bus import EventBus, AudioCaptured, MicrophoneDisconnected, MicrophoneReconnected
from .audio_health import AudioHealth
from .audio_statistics import AudioStatistics

class AudioCapture:
    def __init__(self, mic: MicrophoneManager, buffer: AudioBuffer, event_bus: EventBus, health: AudioHealth, stats: AudioStatistics):
        self.mic = mic
        self.buffer = buffer
        self.event_bus = event_bus
        self.health = health
        self.stats = stats
        self.log = Logger.get("AudioCapture")
        self.loop = asyncio.get_running_loop()
        self._running = False
        self._task = None

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._capture_loop())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _capture_loop(self):
        while self._running:
            try:
                if not self.mic.is_connected:
                    if self.mic.connect():
                        self.mic.reset_backoff()
                        self.event_bus.publish(MicrophoneReconnected())
                        self.health.mic_status = "CONNECTED"
                    else:
                        self.health.mic_status = "DISCONNECTED"
                        await self.mic.wait_before_reconnect()
                        continue

                start_time = time.perf_counter()
                
                # Execute blocking capture in thread pool
                chunk = await self.loop.run_in_executor(None, self.mic.get_chunk)
                
                latency_ms = (time.perf_counter() - start_time) * 1000
                self.health.capture_latency_ms = latency_ms
                self.stats.record_capture(latency_ms)

                if chunk:
                    now = int(time.time() * 1000)
                    self.buffer.push(chunk)
                    self.event_bus.publish(AudioCaptured(timestamp_ms=now))
                else:
                    self.log.warning("Microphone connection lost.")
                    self.mic.disconnect()
                    self.event_bus.publish(MicrophoneDisconnected())

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Audio capture loop error: {e}")
                await asyncio.sleep(1.0)
