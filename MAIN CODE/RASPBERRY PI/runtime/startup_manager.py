"""
startup_manager.py
Recon Rover V1 - Full System Integration

Iterates through the Dependency Graph to safely bring up the entire stack.
"""

import logging
from typing import Dict
from .dependency_graph import DependencyGraph
from .lifecycle_manager import BaseModule

class StartupManager:
    def __init__(self, modules: Dict[str, BaseModule]):
        self.log = logging.getLogger("StartupManager")
        self.modules = modules
        self.sequence = DependencyGraph.get_startup_sequence()
        
    async def execute_startup(self) -> bool:
        self.log.info("Initiating Full System Startup...")
        
        for name in self.sequence:
            if name not in self.modules:
                self.log.error(f"Critical module '{name}' is missing from runtime registry.")
                return False
                
            mod = self.modules[name]
            self.log.info(f"[{name}] -> initialize()")
            try:
                await mod.initialize()
            except Exception as e:
                self.log.error(f"[{name}] Failed to initialize: {e}")
                return False
                
            self.log.info(f"[{name}] -> start()")
            try:
                await mod.start()
            except Exception as e:
                self.log.error(f"[{name}] Failed to start: {e}")
                return False
                
        self.log.info("Full System Startup COMPLETE.")
        return True
