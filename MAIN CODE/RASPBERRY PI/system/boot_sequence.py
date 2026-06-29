"""
boot_sequence.py
Recon Rover V1 - System Orchestrator

Executes deterministic, ordered application startup.
"""

import time
from logger import Logger
from event_bus import EventBus, ApplicationStarting, ApplicationReady, ModuleStarted
from .module_registry import ModuleRegistry
from .application_state import LifecycleState
from .system_statistics import SystemStatistics

class BootSequence:
    def __init__(self, event_bus: EventBus, stats: SystemStatistics):
        self.event_bus = event_bus
        self.stats = stats
        self.log = Logger.get("BootSequence")

    async def execute(self):
        """
        Bootstraps all modules in the registry deterministically.
        Currently relying on registration order for simplicity, but can be 
        expanded to use a dependency graph.
        """
        start_time = time.perf_counter()
        self.stats.record_boot_start()
        
        self.log.info("Initiating Boot Sequence...")
        self.event_bus.publish(ApplicationStarting())
        
        # Phase 1: Initialize all modules
        for name, record in ModuleRegistry._records.items():
            ModuleRegistry.set_state(name, LifecycleState.INITIALIZING)
            if hasattr(record.instance, 'initialize'):
                self.log.info(f"Initializing {name}...")
                try:
                    await record.instance.initialize()
                except Exception as e:
                    self.log.critical(f"Failed to initialize {name}: {e}")
                    ModuleRegistry.set_state(name, LifecycleState.FAILED)
                    self.stats.record_boot_failure()
                    raise

        # Phase 2: Start all modules
        for name, record in ModuleRegistry._records.items():
            if hasattr(record.instance, 'start'):
                self.log.info(f"Starting {name}...")
                try:
                    await record.instance.start()
                    ModuleRegistry.set_state(name, LifecycleState.READY)
                    self.event_bus.publish(ModuleStarted(module_name=name))
                except Exception as e:
                    self.log.critical(f"Failed to start {name}: {e}")
                    ModuleRegistry.set_state(name, LifecycleState.FAILED)
                    self.stats.record_boot_failure()
                    raise
            else:
                ModuleRegistry.set_state(name, LifecycleState.READY)

        # Transition complete
        duration_ms = (time.perf_counter() - start_time) * 1000
        self.stats.record_boot_success(duration_ms, len(ModuleRegistry._records))
        self.log.info(f"Boot Sequence completed in {duration_ms:.2f}ms.")
        self.event_bus.publish(ApplicationReady())
