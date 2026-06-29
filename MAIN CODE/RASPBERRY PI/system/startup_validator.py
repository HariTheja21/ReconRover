"""
startup_validator.py
Recon Rover V1 - System Orchestrator

Validates the system before entering the RUNNING state.
"""

from logger import Logger
from .module_registry import ModuleRegistry
from .application_state import LifecycleState
from event_bus import EventBus, StartupValidationPassed, StartupValidationFailed

class StartupValidator:
    def __init__(self, event_bus: EventBus):
        self.log = Logger.get("StartupValidator")
        self.event_bus = event_bus

    def validate(self) -> bool:
        """
        Runs comprehensive checks before letting the application go live.
        """
        self.log.info("Running pre-flight startup validation...")
        
        # 1. Verify all registered modules are in READY state
        for name, record in ModuleRegistry._records.items():
            if record.state != LifecycleState.READY:
                self.log.critical(f"Validation Failed: Module {name} is in state {record.state.name}, expected READY.")
                self.event_bus.publish(StartupValidationFailed(reason=f"Module {name} not READY"))
                return False
                
        # 2. Add other checks here (e.g. Circular dependency graph check, though DI container prevents most)
        
        self.log.info("Startup validation passed. All systems GO.")
        self.event_bus.publish(StartupValidationPassed())
        return True
