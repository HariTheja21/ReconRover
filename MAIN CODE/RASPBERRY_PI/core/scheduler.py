"""
scheduler.py
Recon Rover V1 - Cognitive Layer

A lightweight asyncio task scheduler for periodic module tasks.
"""

import asyncio
from typing import Callable, Awaitable, List
from lifecycle_manager import BaseModule
from logger import Logger

class Scheduler(BaseModule):
    """
    Manages periodic background tasks.
    """
    def __init__(self):
        super().__init__()
        self._tasks: List[asyncio.Task] = []
        self._running = False

    async def initialize(self):
        self.log.info("Initialized Scheduler.")

    async def start(self):
        self._running = True
        self.log.info("Scheduler started.")

    async def stop(self):
        self._running = False
        self.log.info("Stopping Scheduler tasks...")
        for task in self._tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._tasks.clear()
        self.log.info("Scheduler stopped.")

    def schedule_periodic(self, hz: float, func: Callable[[], Awaitable[None]]):
        """Schedule an async function to run at a specific frequency."""
        if hz <= 0:
            return
            
        period_s = 1.0 / hz

        async def _wrapper():
            while self._running:
                start_time = asyncio.get_event_loop().time()
                try:
                    await func()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    self.log.error(f"Error in periodic task {func.__name__}: {e}")
                
                elapsed = asyncio.get_event_loop().time() - start_time
                sleep_time = period_s - elapsed
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                else:
                    self.log.warning(f"Task {func.__name__} missed deadline by {-sleep_time:.3f}s")
                    await asyncio.sleep(0) # Yield control

        task = asyncio.create_task(_wrapper())
        self._tasks.append(task)
        self.log.debug(f"Scheduled {func.__name__} at {hz} Hz")
