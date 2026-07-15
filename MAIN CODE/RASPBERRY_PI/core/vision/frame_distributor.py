"""
Frame Distributor Module
Recon Rover V2 - Phase 2.7

Extracts frames from the FrameBuffer and syndicates them across the EventBus.
"""

from typing import Any
import asyncio
from .vision_events import FrameAvailable

class FrameDistributor:
    """Consumes the frame buffer and pushes to the bus."""
    
    def __init__(self, event_bus: Any, frame_buffer: Any):
        self._bus = event_bus
        self._buffer = frame_buffer
        self._running = False
        self._task = None
        
    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._distribution_loop())
        
    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            
    async def _distribution_loop(self):
        """Asynchronously pulls frames from buffer and publishes."""
        while self._running:
            item = self._buffer.pop()
            if item:
                frame_id, timestamp_ms, frame_data = item
                event = FrameAvailable(
                    frame_id=frame_id,
                    timestamp_ms=timestamp_ms,
                    frame_data=frame_data
                )
                self._bus.publish(event)
            else:
                # Buffer empty, wait a tiny bit to prevent CPU pinning
                await asyncio.sleep(0.005)
