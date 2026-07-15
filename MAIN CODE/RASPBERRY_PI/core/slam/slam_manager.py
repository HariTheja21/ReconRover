"""
SLAM Manager Module
Recon Rover V2 - Phase 3.5
"""
import asyncio
import time
import threading
from typing import Any

from .slam_engine import SLAMEngine
from .slam_health import SLAMHealth
from .slam_statistics import SLAMStatistics
from .slam_events import CorrectedPoseUpdated, SLAMMapUpdated, LoopClosureDetected

try:
    from core.event_bus import Event
    from core.localization.localization_events import RobotPoseUpdated
    from core.mapping.mapping_events import OccupancyGridUpdated
    from core.fusion.fusion_events import FusedObstacle
except ImportError:
    class Event: pass
    class RobotPoseUpdated: pass
    class OccupancyGridUpdated: pass
    class FusedObstacle: pass

class SLAMManager:
    """The central daemon for the SLAM Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.engine = SLAMEngine()
        self.health = SLAMHealth(self._bus)
        self.stats = SLAMStatistics()
        
        self._running = False
        self._loop_task = None
        
        # Latest states
        self._state_lock = threading.RLock()
        self.raw_pose = {"x": 0.0, "y": 0.0, "theta": 0.0}
        self.latest_obstacle = {}
        self.grid_snapshot = ([], []) # (occupied, free)
        
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
        self._bus.subscribe(OccupancyGridUpdated, self._handle_grid)
        self._bus.subscribe(FusedObstacle, self._handle_obstacle)
        
    async def _handle_pose(self, event: Any):
        with self._state_lock:
            self.raw_pose["x"] = getattr(event, "x", 0.0)
            self.raw_pose["y"] = getattr(event, "y", 0.0)
            self.raw_pose["theta"] = getattr(event, "theta", 0.0)
            
    async def _handle_grid(self, event: Any):
        with self._state_lock:
            occ = getattr(event, "occupied_cells", [])
            free = getattr(event, "free_cells", [])
            self.grid_snapshot = (occ, free)
            
    async def _handle_obstacle(self, event: Any):
        with self._state_lock:
            self.latest_obstacle = {
                "distance": getattr(event, "distance_cm", 0.0),
                "timestamp": time.time()
            }
        
    async def _publish_loop(self):
        """Runs the SLAM alignment math at 10Hz."""
        while self._running:
            with self._state_lock:
                x = self.raw_pose["x"]
                y = self.raw_pose["y"]
                theta = self.raw_pose["theta"]
                obs = self.latest_obstacle
                grid = self.grid_snapshot
                
            cx, cy, ctheta, score, closure = self.engine.process_pose(x, y, theta, obs, grid)
            
            now = time.time()
            
            self._bus.publish(CorrectedPoseUpdated(
                timestamp=now,
                x=cx,
                y=cy,
                theta=ctheta,
                confidence=score
            ))
            
            if closure:
                self.stats.increment_loop_closure()
                self._bus.publish(LoopClosureDetected(
                    timestamp=now,
                    matched_pose=(cx, cy, ctheta),
                    correction_delta=(0.0, 0.0, 0.0) # naive delta in stub
                ))
                
            self._bus.publish(SLAMMapUpdated(
                timestamp=now,
                alignment_score=score
            ))
            
            self.stats.increment_match()
            await asyncio.sleep(0.1) # 10Hz cycle for SLAM correction
