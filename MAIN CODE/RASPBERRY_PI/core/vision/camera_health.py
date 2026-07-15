"""
Camera Health Module
Recon Rover V2 - Phase 2.7

Publishes health snapshots and statistics of the vision pipeline.
"""

from typing import Any
import asyncio
from .camera_statistics import CameraStatistics
from .vision_events import CameraHealthUpdated, CameraStatisticsUpdated

class CameraHealth:
    """Periodically retrieves stats and publishes health events."""
    
    def __init__(self, event_bus: Any, stats: CameraStatistics):
        self._bus = event_bus
        self._stats = stats
        self.is_connected = False
        self.status_msg = "Offline"
        
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
            health_event = CameraHealthUpdated(
                is_connected=self.is_connected,
                status_msg=self.status_msg
            )
            self._bus.publish(health_event)
            
            # Broadcast Stats
            snapshot = self._stats.get_snapshot()
            stats_event = CameraStatisticsUpdated(
                current_fps=snapshot["current_fps"],
                total_frames=snapshot["total_frames"],
                dropped_frames=snapshot["dropped_frames"]
            )
            self._bus.publish(stats_event)
            
            await asyncio.sleep(1.0) # Publish 1Hz
