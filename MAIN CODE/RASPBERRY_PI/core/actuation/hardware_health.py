"""
Hardware Health Module
Recon Rover V2 - Phase 2.8

Publishes health snapshots and statistics of the Actuation Layer.
"""

from typing import Any
import asyncio
from .hardware_statistics import HardwareStatistics
from .actuation_events import HardwareHealthUpdated, HardwareStatisticsUpdated

class HardwareHealth:
    """Periodically retrieves stats and publishes health events."""
    
    def __init__(self, event_bus: Any, stats: HardwareStatistics):
        self._bus = event_bus
        self._stats = stats
        self.is_healthy = True
        self.status_flags = {
            "motors": True,
            "servos": True,
            "oled": True,
            "rgb": True,
            "buzzer": True
        }
        
        self._running = False
        self._task = None
        
    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        
    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            
    async def _monitor_loop(self):
        while self._running:
            # Broadcast Health
            health_event = HardwareHealthUpdated(
                is_healthy=self.is_healthy,
                status_flags=self.status_flags.copy()
            )
            self._bus.publish(health_event)
            
            # Broadcast Stats
            snapshot = self._stats.get_snapshot()
            stats_event = HardwareStatisticsUpdated(
                total_commands_routed=snapshot["total_commands_routed"],
                commands_per_second=snapshot["commands_per_second"]
            )
            self._bus.publish(stats_event)
            
            await asyncio.sleep(1.0) # Publish 1Hz
