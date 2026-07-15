"""
Avoidance Manager Module
Recon Rover V2 - Phase 3.8
"""
import asyncio
import time
import threading
from typing import Any

from .avoidance_engine import AvoidanceEngine
from .avoidance_health import AvoidanceHealth
from .avoidance_statistics import AvoidanceStatistics
from .avoidance_state import AvoidanceState
from .avoidance_events import SafeTrajectoryGenerated, ObstacleAvoided, CollisionPredicted, EmergencyStopRequired

try:
    from core.event_bus import Event
    from core.slam.slam_events import CorrectedPoseUpdated
    from core.fusion.fusion_events import FusedObstacle
    from core.path_planning.planner_events import PathGenerated
except ImportError:
    class Event: pass
    class CorrectedPoseUpdated: pass
    class FusedObstacle: pass
    class PathGenerated: pass

class AvoidanceManager:
    """Daemon for the Dynamic Obstacle Avoidance Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.engine = AvoidanceEngine()
        self.health = AvoidanceHealth(self._bus)
        self.stats = AvoidanceStatistics()
        
        self._state_lock = threading.RLock()
        self.latest_pose = {}
        self.latest_obstacle = {}
        self.latest_path = []
        
        self._running = False
        self._loop_task = None
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._avoidance_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        if self._loop_task:
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        self._bus.subscribe(CorrectedPoseUpdated, self._handle_pose)
        self._bus.subscribe(FusedObstacle, self._handle_obstacle)
        self._bus.subscribe(PathGenerated, self._handle_path)
        
    async def _handle_pose(self, event: Any):
        with self._state_lock:
            self.latest_pose = {
                "x": getattr(event, "x", 0.0),
                "y": getattr(event, "y", 0.0),
                "theta": getattr(event, "theta", 0.0)
            }
            
    async def _handle_obstacle(self, event: Any):
        with self._state_lock:
            self.latest_obstacle = {
                "distance_cm": getattr(event, "distance_cm", 0.0)
            }
            
    async def _handle_path(self, event: Any):
        with self._state_lock:
            self.latest_path = getattr(event, "path", [])
            
    async def _avoidance_loop(self):
        """Runs the high-speed safety loop at 20Hz."""
        while self._running:
            with self._state_lock:
                pose = self.latest_pose.copy()
                obs = self.latest_obstacle.copy()
                path = self.latest_path[:]
                
            state, traj, estop = self.engine.evaluate(pose, obs, path)
            now = time.time()
            
            if estop:
                self.stats.increment_stop()
                self._bus.publish(EmergencyStopRequired(
                    timestamp=now,
                    reason="Critical Safety Bubble Violated"
                ))
            elif state == AvoidanceState.AVOIDING:
                self.stats.increment_collision()
                self._bus.publish(CollisionPredicted(
                    timestamp=now,
                    time_to_collision=0.0, # stub
                    distance_cm=obs.get('distance_cm', 0.0)
                ))
                self._bus.publish(SafeTrajectoryGenerated(
                    timestamp=now,
                    trajectory=traj,
                    speed=0.2 # slower evasive speed
                ))
                
            await asyncio.sleep(0.05) # 20Hz Loop
