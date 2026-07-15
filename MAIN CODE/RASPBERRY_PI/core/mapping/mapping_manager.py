"""
Mapping Manager Module
Recon Rover V2 - Phase 3.4
"""
import asyncio
import time
import threading
from typing import Any

from .mapping_engine import MappingEngine
from .mapping_health import MappingHealth
from .mapping_statistics import MappingStatistics
from .mapping_events import MapUpdated, OccupancyGridUpdated, MapStatisticsUpdated

try:
    from core.event_bus import Event
    from core.localization.localization_events import RobotPoseUpdated
    from core.fusion.fusion_events import FusedObstacle
except ImportError:
    class Event: pass
    class RobotPoseUpdated: pass
    class FusedObstacle: pass

class MappingManager:
    """The central daemon for the Mapping Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.engine = MappingEngine()
        self.health = MappingHealth(self._bus)
        self.stats = MappingStatistics()
        
        self._running = False
        self._loop_task = None
        
        self.current_pose = {"x": 0.0, "y": 0.0, "theta": 0.0, "timestamp": 0.0}
        self._pose_lock = threading.RLock()
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._publish_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        if self._loop_task:
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        self._bus.subscribe(RobotPoseUpdated, self._handle_pose)
        self._bus.subscribe(FusedObstacle, self._handle_obstacle)
        
    async def _handle_pose(self, event: Any):
        with self._pose_lock:
            self.current_pose["x"] = getattr(event, "x", 0.0)
            self.current_pose["y"] = getattr(event, "y", 0.0)
            self.current_pose["theta"] = getattr(event, "theta", 0.0)
            self.current_pose["timestamp"] = time.time()
            
    async def _handle_obstacle(self, event: Any):
        dist = getattr(event, "distance_cm", 0.0)
        with self._pose_lock:
            px = self.current_pose["x"]
            py = self.current_pose["y"]
            ptheta = self.current_pose["theta"]
            
        self.engine.process_fused_obstacle(px, py, ptheta, dist)
        self.stats.increment_processed()
        
    async def _publish_loop(self):
        """Runs the mapping optimization and publication at 5Hz."""
        while self._running:
            occ_count, free_count = self.engine.tick()
            now = time.time()
            
            # Map Stats
            total_cells = occ_count + free_count
            self._bus.publish(MapStatisticsUpdated(
                timestamp=now,
                total_cells=total_cells,
                resolution_cm=self.engine.grid.resolution
            ))
            
            # Full Map Update
            occupied, free = self.engine.grid.get_snapshot()
            self._bus.publish(OccupancyGridUpdated(
                timestamp=now,
                occupied_cells=occupied,
                free_cells=free
            ))
            
            self._bus.publish(MapUpdated(
                timestamp=now,
                map_size=total_cells,
                new_cells_added=0 # Derived logically downstream if needed
            ))
            
            await asyncio.sleep(0.2) # 5Hz cycle to save CPU since maps update slowly
