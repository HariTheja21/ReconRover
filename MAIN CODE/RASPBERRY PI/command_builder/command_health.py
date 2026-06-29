"""
command_health.py
Recon Rover V1 - Command Builder

Monitors queue depths, dropped packets, and validation failures.
"""

from dataclasses import dataclass

@dataclass
class CommandHealthMetrics:
    dropped_commands: int = 0
    validation_failures: int = 0
    emergency_stops_issued: int = 0
    queue_depth: int = 0

class CommandHealthMonitor:
    def __init__(self):
        self.metrics = CommandHealthMetrics()

    def record_drop(self):
        self.metrics.dropped_commands += 1

    def record_validation_failure(self):
        self.metrics.validation_failures += 1
        
    def record_emergency_stop(self):
        self.metrics.emergency_stops_issued += 1
        
    def update_queue_depth(self, depth: int):
        self.metrics.queue_depth = depth
