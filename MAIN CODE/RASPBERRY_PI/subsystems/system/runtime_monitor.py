"""
runtime_monitor.py
Recon Rover V1 - System Orchestrator

Supervises module health and publishes semantic failure events.
"""

import asyncio
from logger import Logger
from event_bus import EventBus, ModuleFailed, ModuleRecovered, SystemHealthy, SystemDegraded, SystemCritical
from .module_registry import ModuleRegistry
from .application_state import LifecycleState
from .system_health import SystemHealth
from .system_statistics import SystemStatistics

class RuntimeMonitor:
    def __init__(self, event_bus: EventBus, health: SystemHealth, stats: SystemStatistics):
        self.event_bus = event_bus
        self.health = health
        self.stats = stats
        self.log = Logger.get("RuntimeMonitor")
        self._running = False
        self._task = None
        self._previous_status = "INITIALIZING"

    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _monitor_loop(self):
        while self._running:
            try:
                # 1. Ask health system to re-evaluate based on registry states
                self.health.update()
                current_status = self.health.metrics.overall_status
                
                # 2. Publish state changes
                if current_status != self._previous_status:
                    if current_status == "HEALTHY":
                        self.event_bus.publish(SystemHealthy())
                    elif current_status == "DEGRADED":
                        self.event_bus.publish(SystemDegraded())
                    elif current_status == "CRITICAL":
                        self.event_bus.publish(SystemCritical())
                        
                    self.log.info(f"System Health changed to {current_status}")
                    self._previous_status = current_status
                
                # Note: Automated recovery (restarting individual modules) would go here.
                # For now we are just monitoring and tracking.
                
                await asyncio.sleep(2.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"RuntimeMonitor loop error: {e}")
                await asyncio.sleep(2.0)
