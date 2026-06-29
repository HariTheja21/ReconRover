"""
system_health.py
Recon Rover V1 - System Orchestrator

Tracks the overall health of the application.
"""

from dataclasses import dataclass
from typing import List
from .module_registry import ModuleRegistry
from .application_state import LifecycleState

@dataclass
class SystemHealthMetrics:
    overall_status: str = "INITIALIZING"
    running_modules: int = 0
    failed_modules: int = 0
    recovery_count: int = 0
    restart_count: int = 0

class SystemHealth:
    def __init__(self):
        self.metrics = SystemHealthMetrics()

    def update(self):
        """Re-evaluates health based on the ModuleRegistry."""
        running = len(ModuleRegistry.get_modules_in_state(LifecycleState.RUNNING))
        failed = len(ModuleRegistry.get_modules_in_state(LifecycleState.FAILED))
        
        self.metrics.running_modules = running
        self.metrics.failed_modules = failed
        
        if failed > 0:
            self.metrics.overall_status = "DEGRADED" if running > 0 else "CRITICAL"
        else:
            self.metrics.overall_status = "HEALTHY"

    def record_recovery(self):
        self.metrics.recovery_count += 1
        
    def record_restart(self):
        self.metrics.restart_count += 1
