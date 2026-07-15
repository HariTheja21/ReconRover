import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self, engine: Any):
        self.engine = engine
        self.mission_queue = asyncio.Queue(maxsize=10)
        
    async def enqueue_mission(self, goal: str, params: dict):
        try:
            self.mission_queue.put_nowait((goal, params))
        except asyncio.QueueFull:
            pass
            
    async def run_mission_loop(self):
        logger.info("Starting Planner Mission Loop")
        while True:
            try:
                goal, params = await self.mission_queue.get()
                await self.engine.process_mission(goal, params)
                self.mission_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Mission Loop: {e}")
                
    async def run_task_loop(self):
        logger.info("Starting Planner Task Loop")
        while True:
            try:
                await self.engine.process_task_loop()
                await asyncio.sleep(0.1) # Throttle
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Task Loop: {e}")
                await asyncio.sleep(1.0)
