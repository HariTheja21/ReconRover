import asyncio
import logging

logger = logging.getLogger(__name__)

class PerceptionScheduler:
    def __init__(self, engine: Any):
        self.engine = engine
        self.queue = asyncio.Queue(maxsize=10)
        
    async def enqueue_data(self, detections, depth_map, robot_pose):
        try:
            self.queue.put_nowait((detections, depth_map, robot_pose))
        except asyncio.QueueFull:
            # Drop older state if overwhelmed
            pass
            
    async def run_loop(self):
        logger.info("Starting Perception Scheduler Loop")
        while True:
            try:
                detections, depth_map, robot_pose = await self.queue.get()
                await self.engine.execute(detections, depth_map, robot_pose)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Perception Scheduler: {e}")
