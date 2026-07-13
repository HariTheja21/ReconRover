"""
frame_capture.py
Recon Rover V1 - Vision Pipeline

Asynchronously captures frames from the CameraManager.
"""

import asyncio
import time
from logger import Logger
from .camera_manager import CameraManager
from .frame_buffer import FrameBuffer
from event_bus import EventBus, FrameCaptured, CameraDisconnected, CameraReconnected
from .vision_health import VisionHealth
from .vision_statistics import VisionStatistics

class FrameCapture:
    def __init__(self, camera: CameraManager, buffer: FrameBuffer, event_bus: EventBus, health: VisionHealth, stats: VisionStatistics):
        self.camera = camera
        self.buffer = buffer
        self.event_bus = event_bus
        self.health = health
        self.stats = stats
        self.log = Logger.get("FrameCapture")
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
                if not self.camera.is_connected:
                    if self.camera.connect():
                        self.camera.reset_backoff()
                        self.event_bus.publish(CameraReconnected())
                        self.health.camera_status = "CONNECTED"
                    else:
                        self.health.camera_status = "DISCONNECTED"
                        await self.camera.wait_before_reconnect()
                        continue

                start_time = time.perf_counter()
                
                # Execute blocking capture in thread pool
                frame = await self.loop.run_in_executor(None, self.camera.get_frame)
                
                latency_ms = (time.perf_counter() - start_time) * 1000
                self.health.capture_latency_ms = latency_ms
                self.stats.record_capture(latency_ms)

                if frame:
                    now = int(time.time() * 1000)
                    self.buffer.push(frame)
                    self.event_bus.publish(FrameCaptured(timestamp_ms=now))
                else:
                    self.log.warning("Camera connection lost.")
                    self.camera.disconnect()
                    self.event_bus.publish(CameraDisconnected())

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Capture loop error: {e}")
                await asyncio.sleep(1.0)
