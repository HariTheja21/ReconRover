"""
Packet Health Module
Recon Rover V2 - Phase 4.3
"""
import asyncio
from typing import Any
from .serial_events import SerialHealthUpdated

class PacketHealth:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.is_healthy = True
        self.status_flags = {"connected": False}
        self._running = False
        
    def set_connected(self, status: bool):
        self.status_flags["connected"] = status
        self.is_healthy = status
        
    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._monitor())
        
    def stop(self):
        self._running = False
        if hasattr(self, '_task'):
            self._task.cancel()
            
    async def _monitor(self):
        while self._running:
            self._bus.publish(SerialHealthUpdated(
                is_healthy=self.is_healthy,
                status_flags=self.status_flags.copy()
            ))
            await asyncio.sleep(5.0)
