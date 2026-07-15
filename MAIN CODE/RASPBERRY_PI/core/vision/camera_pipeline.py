"""
Camera Pipeline Module
Recon Rover V2 - Phase 2.7

The core engine of the vision node. 
Pulls raw frames from hardware, attaches metadata (timestamp, IDs), and pushes them to the buffer.
"""

import time
import asyncio
from typing import Any

from .camera_capture import CameraCapture
from .frame_buffer import FrameBuffer
from .camera_statistics import CameraStatistics
from .vision_events import FrameCaptured, FrameDropped

class CameraPipeline:
    """Manages the raw acquisition loop."""
    
    def __init__(self, event_bus: Any, frame_buffer: FrameBuffer, stats: CameraStatistics, resolution: tuple, fps: int):
        self._bus = event_bus
        self._buffer = frame_buffer
        self._stats = stats
        self.resolution = resolution
        self.fps = fps
        
        self.capture = CameraCapture(resolution=resolution, fps=fps)
        self._running = False
        self._task = None
        self._frame_counter = 0
        
    def start(self) -> bool:
        """Initializes hardware and starts the capture loop."""
        if self.capture.start():
            self._running = True
            self._task = asyncio.create_task(self._capture_loop())
            return True
        return False
        
    def stop(self):
        """Halts the pipeline and releases hardware."""
        self._running = False
        if self._task:
            self._task.cancel()
        self.capture.stop()
        
    async def _capture_loop(self):
        """High-priority loop to pull frames."""
        target_delay = 1.0 / self.fps
        
        while self._running:
            start_time = time.time()
            
            # Blocking hardware read (should be offloaded to thread in production, 
            # but acceptable for cv2.VideoCapture in synthetic testing)
            frame = self.capture.read_frame()
            
            if frame is not None:
                self._frame_counter += 1
                timestamp_ms = int(time.time() * 1000)
                
                # Push to buffer
                dropped = self._buffer.push(self._frame_counter, timestamp_ms, frame)
                if dropped:
                    self._stats.add_drop()
                    self._bus.publish(FrameDropped(frame_id=self._frame_counter, reason="Buffer Overflow"))
                
                self._stats.add_frame()
                self._bus.publish(FrameCaptured(frame_id=self._frame_counter, timestamp_ms=timestamp_ms))
            
            # Rate limiting
            elapsed = time.time() - start_time
            sleep_time = max(0.001, target_delay - elapsed)
            await asyncio.sleep(sleep_time)
