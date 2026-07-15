"""
System Orchestrator Module
Recon Rover V2 - Phase 3.0
"""
from typing import Any
from .runtime_manager import RuntimeManager

class SystemOrchestrator:
    """The highest level application orchestrator. Bootstraps the EventBus and RuntimeManager."""
    
    def __init__(self, event_bus_instance: Any):
        self.event_bus = event_bus_instance
        self.runtime = RuntimeManager(self.event_bus)
        
    def register_subsystem(self, name: str, instance: Any, dependencies: list = None):
        self.runtime.register_module(name, instance, dependencies)
