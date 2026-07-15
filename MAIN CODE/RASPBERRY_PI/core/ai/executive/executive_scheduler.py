import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ExecutiveScheduler:
    def __init__(self, engine: Any):
        self.engine = engine
        
    async def run_executive_loop(self):
        logger.info("Starting Executive Loop")
        while True:
            try:
                await self.engine.run_tick()
                await asyncio.sleep(0.1) # 10Hz supervisor loop
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Executive Loop: {e}")
                await asyncio.sleep(1.0)
