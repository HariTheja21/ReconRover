"""
command_scheduler.py
Recon Rover V1 - Command Builder

Pulls from the CommandQueue and applies rate limits.
"""

import asyncio
from event_bus import EventBus
from .command_queue import CommandQueue
# Assume we will define CommandPacketReady in event_bus
import time

class CommandScheduler:
    """
    Rate limits and dispatches commands.
    """
    def __init__(self, queue: CommandQueue, event_bus: EventBus, rate_limit_ms: int = 20):
        self.queue = queue
        self.event_bus = event_bus
        self.rate_limit_sec = rate_limit_ms / 1000.0
        self._running = False
        self._task = None

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run_loop())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _run_loop(self):
        # We need to import the event dynamically to avoid circular issues or just assume it exists
        from event_bus import CommandPacketReady
        
        while self._running:
            try:
                packet = await self.queue.get()
                
                # Publish the packet to the event bus for the Serial Manager
                self.event_bus.publish(CommandPacketReady(packet=packet))
                self.queue.task_done()
                
                # Rate limit (non-blocking)
                await asyncio.sleep(self.rate_limit_sec)
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Log but continue
                await asyncio.sleep(self.rate_limit_sec)
