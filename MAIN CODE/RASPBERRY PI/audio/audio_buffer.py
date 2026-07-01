"""
audio_buffer.py
Recon Rover V1 - Audio Pipeline

Bounded asynchronous buffer for audio chunks.
"""

import asyncio
from logger import Logger
from .audio_health import AudioHealth
from .audio_statistics import AudioStatistics

class AudioBuffer:
    def __init__(self, health: AudioHealth, stats: AudioStatistics, maxsize: int = 5):
        self.queue = asyncio.Queue(maxsize=maxsize)
        self.health = health
        self.stats = stats
        self.log = Logger.get("AudioBuffer")

    def push(self, chunk: bytes):
        """Pushes an audio chunk to the buffer. Drops the oldest if full."""
        if self.queue.full():
            try:
                self.queue.get_nowait()
                self.stats.record_dropped_chunk()
                self.log.debug("Audio buffer full. Dropped oldest chunk.")
            except asyncio.QueueEmpty:
                self.log.debug("Queue was concurrently emptied.")
        
        try:
            self.queue.put_nowait(chunk)
        except asyncio.QueueFull:
            self.log.warning("Audio buffer full after eviction. Dropping current chunk.")
            
        self.health.buffer_utilization = self.queue.qsize() / self.queue.maxsize

    async def get(self) -> bytes:
        chunk = await self.queue.get()
        self.health.buffer_utilization = self.queue.qsize() / self.queue.maxsize
        return chunk

    def task_done(self):
        self.queue.task_done()
