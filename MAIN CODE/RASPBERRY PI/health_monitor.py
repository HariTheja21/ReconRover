"""
health_monitor.py
Recon Rover V1 - Cognitive Layer

Monitors system health and fault events, triggering safe mode if needed.
"""

from lifecycle_manager import BaseModule
from event_bus import EventBus, FaultReceived, HealthUpdate, CommandIssued
from module_registry import ModuleRegistry

class HealthMonitor(BaseModule):
    """
    Monitors overall system health.
    """
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus

    async def initialize(self):
        self.event_bus.subscribe(FaultReceived, self._on_fault)
        self.log.info("Health Monitor initialized.")

    async def start(self):
        self.log.info("Health Monitor active.")

    async def stop(self):
        self.log.info("Health Monitor stopped.")

    async def check_modules(self):
        """Periodic health check of all registered modules."""
        modules = ModuleRegistry.all_modules()
        all_ok = True
        
        for name, module in modules.items():
            if hasattr(module, 'health'):
                try:
                    status = module.health()
                    if status != "OK":
                        self.log.warning(f"Module {name} reports unhealthy: {status}")
                        all_ok = False
                        self.event_bus.publish(HealthUpdate(module_name=name, status="WARN", details=status))
                except Exception as e:
                    self.log.error(f"Failed to get health from {name}: {e}")
                    all_ok = False
        
        if not all_ok:
            self._trigger_safe_mode()

    async def _on_fault(self, event: FaultReceived):
        self.log.error(f"Critical fault received from subsystem {event.subsystem}, code: {event.code}")
        self._trigger_safe_mode()

    def _trigger_safe_mode(self):
        self.log.critical("TRIGGERING SYSTEM SAFE MODE")
        # Publish an E-STOP command to the CommandDispatcher
        cmd = CommandIssued(
            command_type="EMERGENCY_STOP",
            payload={}
        )
        self.event_bus.publish(cmd)
