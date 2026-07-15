"""
Navigation Manager Module
Recon Rover V2 - Phase 3.6
"""
import asyncio
import time
from typing import Any

from .navigation_engine import NavigationEngine
from .navigation_health import NavigationHealth
from .navigation_statistics import NavigationStatistics
from .navigation_events import NavigationStateUpdated, GoalReached, WaypointReached, GoalUpdated
from .navigation_state import NavigationState

try:
    from core.event_bus import Event
    from core.slam.slam_events import CorrectedPoseUpdated
    from core.mapping.mapping_events import OccupancyGridUpdated
except ImportError:
    class Event: pass
    class CorrectedPoseUpdated: pass
    class OccupancyGridUpdated: pass

class NavigationManager:
    """The central daemon for the Navigation Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.engine = NavigationEngine()
        self.health = NavigationHealth(self._bus)
        self.stats = NavigationStatistics()
        
        self._running = False
        self._loop_task = None
        
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
        self._bus.subscribe(CorrectedPoseUpdated, self._handle_pose)
        self._bus.subscribe(OccupancyGridUpdated, self._handle_grid)
        self._bus.subscribe(GoalUpdated, self._handle_new_goal)
        
    async def _handle_pose(self, event: Any):
        x = getattr(event, "x", 0.0)
        y = getattr(event, "y", 0.0)
        theta = getattr(event, "theta", 0.0)
        self.engine.context.update_pose(x, y, theta)
        
    async def _handle_grid(self, event: Any):
        occ = getattr(event, "occupied_cells", [])
        free = getattr(event, "free_cells", [])
        self.engine.context.update_map(occ, free)
        
    async def _handle_new_goal(self, event: Any):
        gid = getattr(event, "goal_id", "default")
        x = getattr(event, "target_x", 0.0)
        y = getattr(event, "target_y", 0.0)
        
        # Reset state to accept new goal
        self.engine.state.set_state(NavigationState.IDLE)
        self.engine.goal.set_goal(gid, x, y)
        
    async def _publish_loop(self):
        """Runs the navigation state machine at 10Hz."""
        while self._running:
            state, target, wp_reached, gl_reached = self.engine.tick()
            now = time.time()
            
            self._bus.publish(NavigationStateUpdated(
                timestamp=now,
                state=state,
                current_target=target
            ))
            
            if wp_reached and target:
                self.stats.increment_waypoint()
                self._bus.publish(WaypointReached(
                    timestamp=now,
                    waypoint_index=self.engine.waypoints.current_index - 1,
                    waypoint_pose=target
                ))
                
            if gl_reached:
                self.stats.increment_goal()
                gid = self.engine.goal.active_goal_id
                # The final target is cached in the goal manager
                gx, gy = self.engine.goal.target_x, self.engine.goal.target_y
                self._bus.publish(GoalReached(
                    timestamp=now,
                    goal_id=gid,
                    target_pose=(gx, gy)
                ))
                
            await asyncio.sleep(0.1) # 10Hz cycle
