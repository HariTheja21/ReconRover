"""
Runtime Health Module
Recon Rover V2 - Phase 3.0
"""
from typing import Any
from .runtime_events import RuntimeHealthy, RuntimeFault

class RuntimeHealth:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.is_healthy = True
        self.faults = set()
        
    def set_fault(self, module_name: str):
        self.faults.add(module_name)
        self.is_healthy = False
        self._bus.publish(RuntimeFault(faulting_modules=list(self.faults)))
        self._bus.publish(RuntimeHealthy(is_healthy=False))
        
    def clear_fault(self, module_name: str):
        if module_name in self.faults:
            self.faults.remove(module_name)
        if not self.faults:
            self.is_healthy = True
            self._bus.publish(RuntimeHealthy(is_healthy=True))
