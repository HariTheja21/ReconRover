import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ExplorationScheduler:
    def __init__(self, engine: Any):
        self.engine = engine
        self.grid_queue = asyncio.Queue(maxsize=10)
        
    async def enqueue_grid(self, grid: Any, resolution: float, origin: tuple):
        try:
            self.grid_queue.put_nowait((grid, resolution, origin))
        except asyncio.QueueFull:
            pass # Drop frame to prevent backpressure
            
    async def run_loop(self):
        logger.info("Starting Exploration AI Loop")
        while True:
            try:
                grid, res, origin = await self.grid_queue.get()
                await self.engine.process_grid_update(grid, res, origin)
                self.grid_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Exploration AI Loop: {e}")
