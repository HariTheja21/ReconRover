"""
Motion Manager Module
Recon Rover V2 - Phase 4.0
"""
import asyncio
import time
import threading
from typing import Any

from .motion_engine import MotionEngine
from .motion_health import MotionHealth
from .motion_statistics import MotionStatistics
from .motion_context import MotionContext
from .motion_state import MotionState
from .motion_events import (MotionRequest, MotionStopped, MotionPaused, 
                          MotionResumed, MotionStateUpdated)

try:
    from core.event_bus import Event
    from core.navigation.navigation_events import NavigationStateUpdated
    from core.obstacle_avoidance.avoidance_events import SafeTrajectoryGenerated, EmergencyStopRequired
    from core.mission.mission_events import MissionStarted, MissionPaused, MissionCancelled
except ImportError:
    class Event: pass
    class NavigationStateUpdated: pass
    class SafeTrajectoryGenerated: pass
    class EmergencyStopRequired: pass
    class MissionStarted: pass
    class MissionPaused: pass
    class MissionCancelled: pass

class MotionManager:
    """Daemon for the Motion Controller."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = MotionStatistics()
        self.engine = MotionEngine(self.stats)
        self.health = MotionHealth(self._bus)
        self.context = MotionContext()
        
        self._state_lock = threading.RLock()
        self.target_lin = 0.0
        self.target_ang = 0.0
        
        self._running = False
        self._loop_task = None
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._motion_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        if self._loop_task:
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        # We listen to SafeTrajectoryGenerated for evasive overrides.
        # In a full system, Navigation core might also emit basic target speeds.
        # For Phase 4.0, we just map abstract inputs.
        self._bus.subscribe(SafeTrajectoryGenerated, self._handle_safe_traj)
        
        # Mission / Navigation Context
        self._bus.subscribe(MissionStarted, self._handle_mission_start)
        self._bus.subscribe(MissionPaused, self._handle_mission_pause)
        self._bus.subscribe(MissionCancelled, self._handle_mission_cancel)
        self._bus.subscribe(EmergencyStopRequired, self._handle_estop)
        
    async def _handle_safe_traj(self, event: Any):
        with self._state_lock:
            # Stub: in reality, we would extract required linear/angular speeds from the trajectory
            self.target_lin = getattr(event, "speed", 0.0)
            self.target_ang = 0.0 # pure forward dodge stub
            
    async def _handle_mission_start(self, event: Any):
        self.context.set("mission_active", True)
        self.context.set("paused", False)
        
    async def _handle_mission_pause(self, event: Any):
        self.context.set("paused", True)
        self._bus.publish(MotionPaused(timestamp=time.time()))
        
    async def _handle_mission_cancel(self, event: Any):
        self.context.set("mission_active", False)
        self.context.set("paused", False)
        self._bus.publish(MotionStopped(timestamp=time.time(), reason="Mission Cancelled"))
        
    async def _handle_estop(self, event: Any):
        self.context.set("estop", True)
        self._bus.publish(MotionStopped(timestamp=time.time(), reason="Emergency Stop"))
        
    # Allows external testing injection of targets
    def inject_target(self, lin: float, ang: float):
        with self._state_lock:
            self.target_lin = lin
            self.target_ang = ang
            
    async def _motion_loop(self):
        """Runs the high-speed motion evaluation loop at 20Hz."""
        last_state = self.engine.state.get()
        while self._running:
            with self._state_lock:
                t_lin = self.target_lin
                t_ang = self.target_ang
                
            ctx = self.context.context.copy()
            safe_lin, safe_ang, limited = self.engine.evaluate(t_lin, t_ang, ctx)
            
            now = time.time()
            
            self.stats.increment_processed()
            if limited:
                self.stats.increment_limited()
                
            # Publish if we are actually requesting movement or actively stopped due to estop
            if self.engine.state.get() in [MotionState.ACTIVE, MotionState.ESTOP]:
                self._bus.publish(MotionRequest(
                    timestamp=now,
                    linear_velocity=safe_lin,
                    angular_velocity=safe_ang
                ))
                
            current_state = self.engine.state.get()
            if current_state != last_state:
                self._bus.publish(MotionStateUpdated(timestamp=now, state=current_state))
                last_state = current_state
                
            await asyncio.sleep(0.05) # 20Hz loop
