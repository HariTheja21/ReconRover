"""
Kinematics Manager Module
Recon Rover V2 - Phase 4.1
"""
import asyncio
import time
import threading
from typing import Any

from .kinematics_engine import KinematicsEngine
from .kinematics_health import KinematicsHealth
from .kinematics_statistics import KinematicsStatistics
from .kinematics_events import WheelVelocityRequest, KinematicsUpdated

try:
    from core.event_bus import Event
    from core.motion.motion_events import MotionRequest, MotionStopped, MotionPaused
    from core.obstacle_avoidance.avoidance_events import EmergencyStopRequired
except ImportError:
    class Event: pass
    class MotionRequest: pass
    class MotionStopped: pass
    class MotionPaused: pass
    class EmergencyStopRequired: pass

class KinematicsManager:
    """Daemon for the Kinematics Controller."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = KinematicsStatistics()
        self.engine = KinematicsEngine(self.stats)
        self.health = KinematicsHealth(self._bus)
        
        self._state_lock = threading.RLock()
        self.target_lin = 0.0
        self.target_ang = 0.0
        self._new_data = False
        
        self._running = False
        self._loop_task = None
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._kinematics_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        if self._loop_task:
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        self._bus.subscribe(MotionRequest, self._handle_motion_request)
        self._bus.subscribe(MotionStopped, self._handle_motion_stopped)
        self._bus.subscribe(MotionPaused, self._handle_motion_paused)
        self._bus.subscribe(EmergencyStopRequired, self._handle_estop)
        
    async def _handle_motion_request(self, event: Any):
        with self._state_lock:
            self.target_lin = getattr(event, "linear_velocity", 0.0)
            self.target_ang = getattr(event, "angular_velocity", 0.0)
            self._new_data = True
            
    async def _handle_motion_stopped(self, event: Any):
        with self._state_lock:
            self.target_lin = 0.0
            self.target_ang = 0.0
            self._new_data = True
            
    async def _handle_motion_paused(self, event: Any):
        with self._state_lock:
            self.target_lin = 0.0
            self.target_ang = 0.0
            self._new_data = True
            
    async def _handle_estop(self, event: Any):
        self.engine.set_estop()
        with self._state_lock:
            self.target_lin = 0.0
            self.target_ang = 0.0
            self._new_data = True
            
    # Allows external testing injection of targets
    def inject_target(self, lin: float, ang: float):
        with self._state_lock:
            self.target_lin = lin
            self.target_ang = ang
            self._new_data = True
            
    async def _kinematics_loop(self):
        """Runs the high-speed kinematics evaluation loop at 20Hz."""
        last_state = self.engine.state.get()
        while self._running:
            with self._state_lock:
                has_new = self._new_data
                t_lin = self.target_lin
                t_ang = self.target_ang
                self._new_data = False
                
            if has_new:
                vl, vr, valid = self.engine.evaluate(t_lin, t_ang)
                now = time.time()
                
                if valid:
                    self._bus.publish(WheelVelocityRequest(
                        timestamp=now,
                        left_velocity=vl,
                        right_velocity=vr
                    ))
                    
                current_state = self.engine.state.get()
                if current_state != last_state:
                    self._bus.publish(KinematicsUpdated(timestamp=now, state=current_state))
                    last_state = current_state
                    
            await asyncio.sleep(0.05) # 20Hz loop
