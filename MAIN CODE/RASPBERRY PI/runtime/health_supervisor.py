"""
health_supervisor.py
Recon Rover V1 - Full System Integration

Continuously polls the .health() method of all modules to catch hidden failures.
"""

import logging
import asyncio
from typing import Dict
from .lifecycle_manager import BaseModule

class HealthSupervisor:
    def __init__(self, modules: Dict[str, BaseModule]):
        self.log = logging.getLogger("HealthSupervisor")
        self.modules = modules
        self._running = False
        self._task = None
        
    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        
    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            
    async def _monitor_loop(self):
        while self._running:
            for name, mod in self.modules.items():
                try:
                    status = mod.health()
                    if status == "FATAL":
                        self.log.critical(f"MODULE CRASH DETECTED: {name} reported FATAL.")
                        # In a full system, this would trigger the ShutdownManager
                    elif status.startswith("DEGRADED"):
                        self.log.warning(f"MODULE DEGRADED: {name} -> {status}")
                except Exception as e:
                    self.log.error(f"Failed to poll health for {name}: {e}")
                    
            await asyncio.sleep(1.0)
