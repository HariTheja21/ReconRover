"""
runtime_manager.py
Recon Rover V1 - Full System Integration

Coordinates the startup, monitoring, and shutdown of the entire software stack.
"""

import logging
import asyncio
from typing import Dict
from event_bus import EventBus

from .lifecycle_manager import BaseModule
from .startup_manager import StartupManager
from .shutdown_manager import ShutdownManager
from .health_supervisor import HealthSupervisor
from .runtime_statistics import RuntimeStatistics
from .runtime_monitor import RuntimeMonitor
from .integration_validator import IntegrationValidator

class RuntimeManager:
    def __init__(self, modules: Dict[str, BaseModule], event_bus: EventBus):
        self.log = logging.getLogger("RuntimeManager")
        self.modules = modules
        self.event_bus = event_bus
        
        self.startup = StartupManager(self.modules)
        self.shutdown = ShutdownManager(self.modules)
        self.supervisor = HealthSupervisor(self.modules)
        self.validator = IntegrationValidator(self.modules)
        
        self.stats = RuntimeStatistics()
        self.monitor = RuntimeMonitor(self.event_bus, self.stats, self.supervisor)
        
    async def boot_system(self) -> bool:
        """Boots the entire Recon Rover stack."""
        success = await self.startup.execute_startup()
        if not success:
            self.log.critical("Boot Sequence FAILED. Aborting.")
            return False
            
        if not self.validator.validate_integration():
            self.log.critical("Integration Validation FAILED. Aborting.")
            return False
            
        self.supervisor.start()
        self.monitor.start()
        
        self.log.info("System is fully ALIVE and integrated.")
        return True
        
    async def halt_system(self):
        """Safely tears down the stack."""
        self.log.info("Halting System...")
        self.supervisor.stop()
        self.monitor.stop()
        
        await self.shutdown.execute_shutdown()
        self.log.info("System HALTED safely.")
