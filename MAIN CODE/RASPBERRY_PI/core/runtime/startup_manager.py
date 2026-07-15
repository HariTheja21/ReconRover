"""
Startup Manager Module
Recon Rover V2 - Phase 3.0
"""
from typing import Any
from .lifecycle_manager import LifecycleManager, ModuleState
from .dependency_manager import DependencyManager
from .runtime_events import ModuleStarted, SystemStarted

class StartupManager:
    def __init__(self, event_bus: Any, lifecycle: LifecycleManager, deps: DependencyManager):
        self._bus = event_bus
        self.lifecycle = lifecycle
        self.deps = deps
        
    async def boot_system(self):
        order = self.deps.resolve_order()
        
        for name in order:
            instance = self.deps.modules[name]
            self.lifecycle.set_state(name, ModuleState.STARTING)
            
            try:
                # Duck typing: if start() is async, await it
                if hasattr(instance, "start"):
                    start_method = instance.start()
                    if hasattr(start_method, "__await__"):
                        await start_method
                        
                self.lifecycle.set_state(name, ModuleState.RUNNING)
                self._bus.publish(ModuleStarted(module_name=name))
                
            except Exception as e:
                self.lifecycle.set_state(name, ModuleState.FAULT)
                raise RuntimeError(f"Failed to start {name}: {e}")
                
        self._bus.publish(SystemStarted())
