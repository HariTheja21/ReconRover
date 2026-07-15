"""
Sensor Health Module
Recon Rover V2 - Phase 2.9
"""

import asyncio
from typing import Any
from .sensor_statistics import SensorStatistics
from .sensor_events import SensorHealthUpdated, SensorStatisticsUpdated

class SensorHealth:
    def __init__(self, event_bus: Any, stats: SensorStatistics):
        self._bus = event_bus
        self._stats = stats
        self.is_healthy = True
        self.status_flags = {
            "router": True,
            "imu": True,
            "ultrasonic": True,
            "lidar": True,
            "battery": True
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
            health_event = SensorHealthUpdated(
                is_healthy=self.is_healthy,
                status_flags=self.status_flags.copy()
            )
            self._bus.publish(health_event)
            
            # Broadcast Stats
            snapshot = self._stats.get_snapshot()
            stats_event = SensorStatisticsUpdated(
                total_packets_decoded=snapshot["total_packets_decoded"],
                packets_per_second=snapshot["packets_per_second"]
            )
            self._bus.publish(stats_event)
            
            await asyncio.sleep(1.0)
