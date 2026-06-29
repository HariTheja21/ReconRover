"""
frame_provider.py
Recon Rover V1 - Vision Pipeline

Asynchronously pulls frames from the camera manager and places them in the bounded buffer.
Replaces the legacy frame_capture.py.
"""

import asyncio
import time
from logger import Logger
from event_bus import EventBus
from .camera_manager import CameraManager
from .frame_buffer import FrameBuffer
from .vision_health import VisionHealth
from .vision_statistics import VisionStatistics

class FrameProvider:
    def __init__(self, camera: CameraManager, buffer: FrameBuffer, event_bus: EventBus, health: VisionHealth, stats: VisionStatistics):
        self.camera = camera
        self.buffer = buffer
        self.event_bus = event_bus
        self.health = health
        self.stats = stats
        self.log = Logger.get("FrameProvider")
        
        self._running = False
        self._task = None

    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._capture_loop())
        self.log.info("FrameProvider started.")

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("FrameProvider stopped.")

    async def _capture_loop(self):
        while self._running:
            try:
                frame = await self.camera.read_frame()
                if frame is not None:
                    timestamp = time.perf_counter()
                    # Non-blocking put with eviction of oldest if full
                    self.buffer.put_nowait({"frame": frame, "timestamp": timestamp})
                    self.stats.record_captured()
                    
                # Yield to event loop, maintaining rough FPS constraint
                await asyncio.sleep(1.0 / self.camera.fps)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"FrameProvider loop error: {e}")
                self.health.camera_status = "ERROR"
                await asyncio.sleep(1.0)
