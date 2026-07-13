"""
shutdown_sequence.py
Recon Rover V1 - System Orchestrator

Executes deterministic, reverse-ordered application shutdown.
"""

import time
import asyncio
from logger import Logger
from event_bus import EventBus, ApplicationStopping, ApplicationStopped, ModuleStopped
from .module_registry import ModuleRegistry
from .application_state import LifecycleState
from .system_statistics import SystemStatistics

class ShutdownSequence:
    def __init__(self, event_bus: EventBus, stats: SystemStatistics):
        self.event_bus = event_bus
        self.stats = stats
        self.log = Logger.get("ShutdownSequence")

    async def execute(self):
        """
        Stops all modules gracefully in reverse order of registration.
        Includes a timeout to prevent deadlocks from orphaned tasks.
        """
        start_time = time.perf_counter()
        
        self.log.info("Initiating Shutdown Sequence...")
        self.event_bus.publish(ApplicationStopping())
        
        # Shutdown in reverse order
        for name, record in reversed(list(ModuleRegistry._records.items())):
            ModuleRegistry.set_state(name, LifecycleState.STOPPING)
            if hasattr(record.instance, 'stop'):
                self.log.info(f"Stopping {name}...")
                try:
                    # Enforce a 5 second timeout on any module's stop() method
                    await asyncio.wait_for(record.instance.stop(), timeout=5.0)
                    ModuleRegistry.set_state(name, LifecycleState.STOPPED)
                    self.event_bus.publish(ModuleStopped(module_name=name))
                except asyncio.TimeoutError:
                    self.log.error(f"Timeout while stopping {name}. Forcing stop.")
                    ModuleRegistry.set_state(name, LifecycleState.FAILED)
                except Exception as e:
                    self.log.error(f"Error while stopping {name}: {e}")
                    ModuleRegistry.set_state(name, LifecycleState.FAILED)
            else:
                ModuleRegistry.set_state(name, LifecycleState.STOPPED)

        duration_ms = (time.perf_counter() - start_time) * 1000
        self.stats.record_shutdown(duration_ms)
        self.log.info(f"Shutdown Sequence completed in {duration_ms:.2f}ms.")
        self.event_bus.publish(ApplicationStopped())
