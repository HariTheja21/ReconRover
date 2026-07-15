"""
Runtime Manager Module
Recon Rover V2 - Phase 3.0
"""
from typing import Any
import asyncio
from .lifecycle_manager import LifecycleManager
from .dependency_manager import DependencyManager
from .startup_manager import StartupManager
from .shutdown_manager import ShutdownManager
from .module_supervisor import ModuleSupervisor
from .runtime_health import RuntimeHealth
from .runtime_statistics import RuntimeStatistics
from .runtime_events import SystemStartRequest, SystemShutdownRequest

class RuntimeManager:
    """The central runtime hub."""
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.lifecycle = LifecycleManager()
        self.deps = DependencyManager()
        self.health = RuntimeHealth(self._bus)
        self.stats = RuntimeStatistics()
        
        self.startup = StartupManager(self._bus, self.lifecycle, self.deps)
        self.shutdown = ShutdownManager(self._bus, self.lifecycle, self.deps)
        self.supervisor = ModuleSupervisor(self._bus, self.lifecycle, self.deps, self.health, self.stats)
        
        self._bus.subscribe(SystemStartRequest, self._on_start)
        self._bus.subscribe(SystemShutdownRequest, self._on_shutdown)
        
    def register_module(self, name: str, instance: Any, deps: list = None):
        self.lifecycle.register_module(name)
        self.deps.register(name, instance, deps)
        
    async def _on_start(self, event: Any):
        await self.startup.boot_system()
        
    async def _on_shutdown(self, event: Any):
        await self.shutdown.shutdown_system()
