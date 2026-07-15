import asyncio
from typing import Callable
import logging

logger = logging.getLogger(__name__)

class VisionScheduler:
    def __init__(self, worker: Any):
        self.worker = worker
        self.queue = asyncio.Queue(maxsize=5) # Prevent memory ballooning from frame backlog
        
    async def enqueue_frame(self, frame, model_name: str):
        try:
            self.queue.put_nowait((frame, model_name))
        except asyncio.QueueFull:
            # Drop frame if we can't keep up (real-time requirement)
            if hasattr(self.worker, 'stats'):
                self.worker.stats.frames_dropped += 1
                
    async def run_loop(self):
        logger.info("Starting Vision Scheduler Loop")
        while True:
            try:
                frame, model_name = await self.queue.get()
                await self.worker.execute(frame, model_name)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Vision Scheduler: {e}")
