"""
Module Supervisor Module
Recon Rover V2 - Phase 3.0
"""
from typing import Any
import asyncio
from .lifecycle_manager import LifecycleManager, ModuleState
from .dependency_manager import DependencyManager
from .runtime_health import RuntimeHealth
from .runtime_statistics import RuntimeStatistics
from .runtime_events import ModuleRestarted, ModuleFailure, HeartbeatTimeout

class ModuleSupervisor:
    """Listens for faults and restarts modules."""
    
    def __init__(self, event_bus: Any, lifecycle: LifecycleManager, deps: DependencyManager, health: RuntimeHealth, stats: RuntimeStatistics):
        self._bus = event_bus
        self.lifecycle = lifecycle
        self.deps = deps
        self.health = health
        self.stats = stats
        
        self._bus.subscribe(ModuleFailure, self._handle_failure)
        self._bus.subscribe(HeartbeatTimeout, self._handle_timeout)
        
    async def _handle_failure(self, event: Any):
        await self.restart_module(event.module_name)
        
    async def _handle_timeout(self, event: Any):
        await self.restart_module(event.module_name)
        
    async def restart_module(self, module_name: str):
        if module_name not in self.deps.modules:
            return
            
        self.health.set_fault(module_name)
        self.lifecycle.set_state(module_name, ModuleState.STOPPING)
        
        instance = self.deps.modules[module_name]
        
        # Stop
        try:
            if hasattr(instance, "stop"):
                stop_m = instance.stop()
                if hasattr(stop_m, "__await__"):
                    await stop_m
        except Exception:
            pass
            
        await asyncio.sleep(0.5) # cooling
        
        # Start
        self.lifecycle.set_state(module_name, ModuleState.STARTING)
        try:
            if hasattr(instance, "start"):
                start_m = instance.start()
                if hasattr(start_m, "__await__"):
                    await start_m
            
            self.lifecycle.set_state(module_name, ModuleState.RUNNING)
            self.stats.increment_restart(module_name)
            self.health.clear_fault(module_name)
            self._bus.publish(ModuleRestarted(module_name=module_name))
        except Exception as e:
            self.lifecycle.set_state(module_name, ModuleState.FAULT)
