"""
Command Scheduler Module
Recon Rover V2 - Phase 2.5

An asynchronous background loop that consumes the PriorityQueue 
and dispatches OutgoingCommandPackets to the EventBus.
"""

import asyncio
from typing import Any
from .command_queue import CommandQueue
from .command_statistics import CommandStatistics
from .command_events import CommandSent, OutgoingCommandPacket

class CommandScheduler:
    """
    Background worker that routes finalized packets to the physical HAL via the EventBridge.
    """
    
    def __init__(self, event_bus: Any, queue: CommandQueue, stats: CommandStatistics, rate_limit_ms: int = 10):
        self._bus = event_bus
        self._queue = queue
        self._stats = stats
        self.rate_limit_ms = rate_limit_ms
        self._running = False
        self._task = None
        
    def start(self):
        """Starts the async dispatch loop."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._dispatch_loop())
        
    def stop(self):
        """Signals the loop to stop."""
        self._running = False
        if self._task:
            self._task.cancel()
            
    async def _dispatch_loop(self):
        """Pulls packets from the priority queue and publishes them."""
        while self._running:
            try:
                # Wait for the next packet
                packet: OutgoingCommandPacket = await self._queue.get_next()
                
                # Publish to the EventBridge (HAL)
                self._bus.publish(packet)
                self._stats.add_sent()
                
                # Acknowledge dispatch
                self._bus.publish(CommandSent(
                    command_type=packet.command_type,
                    bytes_sent=len(packet.binary_payload)
                ))
                
                self._queue.task_done()
                
                # Apply rate limiting if requested to prevent overwhelming the ESP32
                if self.rate_limit_ms > 0:
                    await asyncio.sleep(self.rate_limit_ms / 1000.0)
                    
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(0.01)
