"""
Planner Manager Module
Recon Rover V2 - Phase 3.7
"""
import asyncio
import time
import threading
from typing import Any

from .planner_engine import PlannerEngine
from .planner_health import PlannerHealth
from .planner_statistics import PlannerStatistics
from .planner_events import PathGenerated, PathInvalidated
from .planner_state import PlannerState

try:
    from core.event_bus import Event
    from core.slam.slam_events import CorrectedPoseUpdated
    from core.mapping.mapping_events import OccupancyGridUpdated
    from core.navigation.navigation_events import NavigationStateUpdated, GoalUpdated
except ImportError:
    class Event: pass
    class CorrectedPoseUpdated: pass
    class OccupancyGridUpdated: pass
    class NavigationStateUpdated: pass
    class GoalUpdated: pass

class PlannerManager:
    """Daemon for the Path Planning Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.engine = PlannerEngine()
        self.health = PlannerHealth(self._bus)
        self.stats = PlannerStatistics()
        
        self._state_lock = threading.RLock()
        self.latest_pose = (0.0, 0.0)
        self.latest_grid = ([], [])
        self.active_goal_id = None
        self.active_goal_target = None
        
        # We only plan when explicitly asked or when map invalidates current path
        self.dirty_flag = False
        
        self._running = False
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._planner_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        if hasattr(self, '_loop_task'):
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        self._bus.subscribe(CorrectedPoseUpdated, self._handle_pose)
        self._bus.subscribe(OccupancyGridUpdated, self._handle_grid)
        self._bus.subscribe(GoalUpdated, self._handle_goal)
        
    async def _handle_pose(self, event: Any):
        with self._state_lock:
            x = getattr(event, "x", 0.0)
            y = getattr(event, "y", 0.0)
            self.latest_pose = (x, y)
            
    async def _handle_grid(self, event: Any):
        with self._state_lock:
            occ = getattr(event, "occupied_cells", [])
            free = getattr(event, "free_cells", [])
            self.latest_grid = (occ, free)
            # In production, check if current path is invalidated here, then set dirty_flag.
            
    async def _handle_goal(self, event: Any):
        with self._state_lock:
            self.active_goal_id = getattr(event, "goal_id", "default")
            tx = getattr(event, "target_x", 0.0)
            ty = getattr(event, "target_y", 0.0)
            self.active_goal_target = (tx, ty)
            self.dirty_flag = True
            
    async def _planner_loop(self):
        """Asynchronous loop checking if a new path calculation is needed."""
        while self._running:
            plan_now = False
            with self._state_lock:
                if self.dirty_flag and self.active_goal_target:
                    plan_now = True
                    self.dirty_flag = False
                    start = self.latest_pose
                    goal = self.active_goal_target
                    grid = self.latest_grid
                    gid = self.active_goal_id
                    
            if plan_now:
                path = self.engine.compute_path(start, goal, grid)
                now = time.time()
                
                if path:
                    self.stats.increment_generated()
                    self._bus.publish(PathGenerated(
                        timestamp=now,
                        goal_id=gid,
                        path=path,
                        cost=len(path) * 1.0 # arbitrary cost placeholder
                    ))
                else:
                    self._bus.publish(PathInvalidated(
                        timestamp=now,
                        reason="No valid path found to goal."
                    ))
                    
            await asyncio.sleep(0.5) # Plan loop checks at 2Hz for trigger
