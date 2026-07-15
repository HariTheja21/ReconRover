"""
Kinematics Health Module
Recon Rover V2 - Phase 4.1
"""
import asyncio
from typing import Any
from .kinematics_events import KinematicsHealthUpdated

class KinematicsHealth:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.is_healthy = True
        self.status_flags = {"kinematics_ready": True}
        self._running = False
        
    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._monitor())
        
    def stop(self):
        self._running = False
        if hasattr(self, '_task'):
            self._task.cancel()
            
    async def _monitor(self):
        while self._running:
            self._bus.publish(KinematicsHealthUpdated(
                is_healthy=self.is_healthy,
                status_flags=self.status_flags.copy()
            ))
            await asyncio.sleep(5.0)
