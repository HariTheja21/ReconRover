"""
frame_buffer.py
Recon Rover V1 - Vision Pipeline

Bounded asynchronous buffer for camera frames.
"""

import asyncio
from logger import Logger
from .vision_health import VisionHealth
from .vision_statistics import VisionStatistics

class FrameBuffer:
    def __init__(self, health: VisionHealth, stats: VisionStatistics, maxsize: int = 5):
        self.queue = asyncio.Queue(maxsize=maxsize)
        self.health = health
        self.stats = stats
        self.log = Logger.get("FrameBuffer")

    def push(self, frame: bytes):
        """Pushes a frame to the buffer. Drops the oldest if full."""
        if self.queue.full():
            try:
                self.queue.get_nowait()
                self.stats.record_dropped_frame()
                self.log.debug("Buffer full. Dropped oldest frame.")
            except asyncio.QueueEmpty:
                self.log.debug("Queue was concurrently emptied.")
        
        try:
            self.queue.put_nowait(frame)
        except asyncio.QueueFull:
            self.log.warning("Vision buffer full after eviction. Dropping current frame.")
            
        self.health.buffer_utilization = self.queue.qsize() / self.queue.maxsize

    async def get(self) -> bytes:
        frame = await self.queue.get()
        self.health.buffer_utilization = self.queue.qsize() / self.queue.maxsize
        return frame

    def task_done(self):
        self.queue.task_done()
