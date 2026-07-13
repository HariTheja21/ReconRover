"""
diagnostics.py
Recon Rover V1 - Cognitive Layer

Collects OS and process-level metrics (CPU, RAM).
"""

import psutil
from lifecycle_manager import BaseModule
from event_bus import EventBus, DiagnosticsUpdate

class Diagnostics(BaseModule):
    """
    Collects system metrics for dashboards.
    """
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self._process = psutil.Process()
        
    async def initialize(self):
        self.log.info("Diagnostics initialized.")

    async def start(self):
        self.log.info("Diagnostics active.")

    async def stop(self):
        self.log.info("Diagnostics stopped.")

    async def gather_metrics(self):
        """Periodic task to gather and publish metrics."""
        cpu = psutil.cpu_percent(interval=None)
        ram = self._process.memory_percent()
        
        # Mock serial latency for now; real latency tracked in SerialManager
        latency = 0.0 
        
        evt = DiagnosticsUpdate(
            cpu_percent=cpu,
            ram_percent=ram,
            serial_latency_ms=latency
        )
        self.event_bus.publish(evt)
        self.log.debug(f"Diagnostics: CPU {cpu}%, RAM {ram:.1f}%")
