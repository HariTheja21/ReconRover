import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class SemanticScheduler:
    def __init__(self, engine: Any):
        self.engine = engine
        self.scene_queue = asyncio.Queue(maxsize=20)
        self.landmark_queue = asyncio.Queue(maxsize=20)
        
    async def enqueue_scene(self, scene_data: dict):
        try:
            self.scene_queue.put_nowait(scene_data)
        except asyncio.QueueFull:
            pass
            
    async def enqueue_landmark(self, name: str, x: float, y: float, z: float):
        try:
            self.landmark_queue.put_nowait((name, x, y, z))
        except asyncio.QueueFull:
            pass
            
    async def run_scene_loop(self):
        logger.info("Starting Semantic Scene Loop")
        while True:
            try:
                scene = await self.scene_queue.get()
                await self.engine.process_scene_update(scene)
                self.scene_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Semantic Scene Loop: {e}")
                
    async def run_landmark_loop(self):
        while True:
            try:
                name, x, y, z = await self.landmark_queue.get()
                await self.engine.create_landmark(name, x, y, z)
                self.landmark_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Semantic Landmark Loop: {e}")
