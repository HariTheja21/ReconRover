"""
shutdown_manager.py
Recon Rover V1 - Full System Integration

Tears down the stack in reverse topological order.
"""

import logging
import asyncio
from typing import Dict
from .dependency_graph import DependencyGraph
from .lifecycle_manager import BaseModule

class ShutdownManager:
    def __init__(self, modules: Dict[str, BaseModule]):
        self.log = logging.getLogger("ShutdownManager")
        self.modules = modules
        self.sequence = DependencyGraph.get_shutdown_sequence()
        
    async def execute_shutdown(self):
        self.log.info("Initiating Full System Graceful Shutdown...")
        
        for name in self.sequence:
            if name in self.modules:
                mod = self.modules[name]
                self.log.info(f"[{name}] -> stop()")
                try:
                    # Impose a 5-second timeout on stop() to prevent hanging
                    await asyncio.wait_for(mod.stop(), timeout=5.0)
                except asyncio.TimeoutError:
                    self.log.error(f"[{name}] Shutdown timed out.")
                except Exception as e:
                    self.log.error(f"[{name}] Shutdown threw exception: {e}")
                    
        self.log.info("Full System Shutdown COMPLETE.")
