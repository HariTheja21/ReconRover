"""
Shutdown Manager Module
Recon Rover V2 - Phase 3.0
"""
from typing import Any
from .lifecycle_manager import LifecycleManager, ModuleState
from .dependency_manager import DependencyManager
from .runtime_events import ModuleStopped, SystemStopped

class ShutdownManager:
    def __init__(self, event_bus: Any, lifecycle: LifecycleManager, deps: DependencyManager):
        self._bus = event_bus
        self.lifecycle = lifecycle
        self.deps = deps
        
    async def shutdown_system(self):
        # Reverse topological order
        order = list(reversed(self.deps.resolve_order()))
        
        for name in order:
            instance = self.deps.modules[name]
            self.lifecycle.set_state(name, ModuleState.STOPPING)
            
            try:
                if hasattr(instance, "stop"):
                    stop_method = instance.stop()
                    if hasattr(stop_method, "__await__"):
                        await stop_method
                        
                self.lifecycle.set_state(name, ModuleState.STOPPED)
                self._bus.publish(ModuleStopped(module_name=name))
            except Exception as e:
                # Log but continue teardown
                print(f"Error stopping {name}: {e}")
                self.lifecycle.set_state(name, ModuleState.FAULT)
                
        self._bus.publish(SystemStopped())
