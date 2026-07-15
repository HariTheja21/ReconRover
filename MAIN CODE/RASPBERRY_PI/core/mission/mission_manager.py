"""
Mission Manager Module
Recon Rover V2 - Phase 3.9
"""
import asyncio
import time
import threading
from typing import Any

from .mission_engine import MissionEngine
from .mission_scheduler import MissionScheduler
from .mission_context import MissionContext
from .mission_health import MissionHealth
from .mission_statistics import MissionStatistics
from .mission_events import (MissionRequest, MissionCancelledRequest, MissionPauseRequest, MissionResumeRequest, 
                           MissionPaused, MissionResumed)

try:
    from core.event_bus import Event
    from core.navigation.navigation_events import NavigationStateUpdated, GoalReached
    from core.obstacle_avoidance.avoidance_events import EmergencyStopRequired
    from core.slam.slam_events import CorrectedPoseUpdated
except ImportError:
    class Event: pass
    class NavigationStateUpdated: pass
    class GoalReached: pass
    class EmergencyStopRequired: pass
    class CorrectedPoseUpdated: pass

class MissionManager:
    """Daemon for the Mission Planner & Execution Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = MissionStatistics()
        self.engine = MissionEngine(self._bus, self.stats)
        self.scheduler = MissionScheduler()
        self.context = MissionContext()
        self.health = MissionHealth(self._bus)
        
        self._running = False
        self._loop_task = None
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._mission_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        if self._loop_task:
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        self._bus.subscribe(MissionRequest, self._handle_mission_request)
        self._bus.subscribe(MissionCancelledRequest, self._handle_cancel_request)
        self._bus.subscribe(MissionPauseRequest, self._handle_pause_request)
        self._bus.subscribe(MissionResumeRequest, self._handle_resume_request)
        
        # Context updates
        self._bus.subscribe(NavigationStateUpdated, self._handle_nav_state)
        self._bus.subscribe(GoalReached, self._handle_goal_reached)
        self._bus.subscribe(EmergencyStopRequired, self._handle_estop)
        self._bus.subscribe(CorrectedPoseUpdated, self._handle_pose)
        
    async def _handle_mission_request(self, event: Any):
        mission = {
            "mission_id": getattr(event, "mission_id", f"m_{time.time()}"),
            "priority": getattr(event, "priority", 10),
            "tasks": getattr(event, "tasks", [])
        }
        self.scheduler.submit_mission(mission)
        
    async def _handle_cancel_request(self, event: Any):
        mid = getattr(event, "mission_id", "")
        if self.engine.active_mission and self.engine.active_mission.get('mission_id') == mid:
            self.engine.cancel()
            self.scheduler.clear_active()
        else:
            self.scheduler.cancel_mission(mid)
            
    async def _handle_pause_request(self, event: Any):
        self.engine.pause()
        if self.engine.active_mission:
            mid = self.engine.active_mission['mission_id']
            self._bus.publish(MissionPaused(timestamp=time.time(), mission_id=mid))
            
    async def _handle_resume_request(self, event: Any):
        self.engine.resume()
        if self.engine.active_mission:
            mid = self.engine.active_mission['mission_id']
            self._bus.publish(MissionResumed(timestamp=time.time(), mission_id=mid))
            
    # Context Handlers
    async def _handle_nav_state(self, event: Any):
        self.context.update("navigation_state", getattr(event, "state", "IDLE"))
        
    async def _handle_goal_reached(self, event: Any):
        self.context.update("goal_reached", True)
        
    async def _handle_estop(self, event: Any):
        self.context.update("emergency_stop", True)
        
    async def _handle_pose(self, event: Any):
        self.context.update("pose", (getattr(event, "x", 0.0), getattr(event, "y", 0.0), getattr(event, "theta", 0.0)))
        
    async def _mission_loop(self):
        """Runs the high-level mission loop at 5Hz."""
        while self._running:
            # 1. Manage Active Mission
            if not self.engine.active_mission:
                next_mission = self.scheduler.get_next_mission()
                if next_mission:
                    self.scheduler.set_active(next_mission)
                    self.engine.load_mission(next_mission)
                    self.engine.start()
            
            # 2. Tick Engine
            if self.engine.active_mission:
                # Provide context snapshot
                ctx = self.context.global_state.copy()
                self.engine.tick(ctx)
                
                # Clear one-shot event flags after tick
                if ctx.get("goal_reached"):
                    self.context.update("goal_reached", False)
                    
            await asyncio.sleep(0.2) # 5Hz Loop
