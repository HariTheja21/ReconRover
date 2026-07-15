import asyncio
import logging
from typing import Callable

logger = logging.getLogger(__name__)

class ShutdownManager:
    def __init__(self):
        self.is_shutting_down = False
        
    async def trigger_shutdown(self, cleanup_callback: Callable):
        self.is_shutting_down = True
        logger.info("Graceful shutdown initiated. Triggering subsystem cleanup...")
        try:
            await cleanup_callback()
            logger.info("Cleanup complete. Halting Ground Station.")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
