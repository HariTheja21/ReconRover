"""
Hardware Bridge Manager Module
Recon Rover V2 - Phase 4.2
"""
import asyncio
import time
import threading
from typing import Any

from .hardware_bridge_engine import HardwareBridgeEngine
from .hardware_bridge_health import HardwareBridgeHealth
from .hardware_bridge_statistics import HardwareBridgeStatistics
from .hardware_bridge_events import (HardwareCommandPacket, HardwareStopPacket, 
                                   HardwareBridgeUpdated)

try:
    from core.event_bus import Event
    from core.kinematics.kinematics_events import WheelVelocityRequest
    from core.motion.motion_events import MotionStopped
    from core.obstacle_avoidance.avoidance_events import EmergencyStopRequired
except ImportError:
    class Event: pass
    class WheelVelocityRequest: pass
    class MotionStopped: pass
    class EmergencyStopRequired: pass

class HardwareBridgeManager:
    """Daemon for the Hardware Execution Bridge."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = HardwareBridgeStatistics()
        self.engine = HardwareBridgeEngine(self.stats)
        self.health = HardwareBridgeHealth(self._bus)
        
        self._state_lock = threading.RLock()
        self.target_l = 0.0
        self.target_r = 0.0
        self._new_data = False
        
        self._running = False
        self._loop_task = None
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._bridge_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        if self._loop_task:
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        self._bus.subscribe(WheelVelocityRequest, self._handle_wheel_req)
        self._bus.subscribe(MotionStopped, self._handle_motion_stopped)
        self._bus.subscribe(EmergencyStopRequired, self._handle_estop)
        
    async def _handle_wheel_req(self, event: Any):
        with self._state_lock:
            self.target_l = getattr(event, "left_velocity", 0.0)
            self.target_r = getattr(event, "right_velocity", 0.0)
            self._new_data = True
            
    async def _handle_motion_stopped(self, event: Any):
        with self._state_lock:
            self.target_l = 0.0
            self.target_r = 0.0
            self._new_data = True
            
    async def _handle_estop(self, event: Any):
        # E-Stop is instantaneous. We don't wait for the loop.
        self.engine.set_estop()
        seq, packet = self.engine.create_stop_packet()
        now = time.time()
        self._bus.publish(HardwareStopPacket(
            timestamp=now,
            sequence_number=seq,
            packet_data=packet,
            reason="Emergency Stop"
        ))
        
    # Allows external testing injection
    def inject_target(self, left: float, right: float):
        with self._state_lock:
            self.target_l = left
            self.target_r = right
            self._new_data = True
            
    async def _bridge_loop(self):
        """Runs the high-speed packet encoding loop at 20Hz."""
        last_state = self.engine.state.get()
        while self._running:
            with self._state_lock:
                has_new = self._new_data
                tl = self.target_l
                tr = self.target_r
                self._new_data = False
                
            if has_new:
                seq, packet = self.engine.evaluate(tl, tr)
                now = time.time()
                
                if packet is not None:
                    self._bus.publish(HardwareCommandPacket(
                        timestamp=now,
                        sequence_number=seq,
                        packet_data=packet
                    ))
                    
            # Check state changes
            current_state = self.engine.state.get()
            if current_state != last_state:
                now = time.time()
                self._bus.publish(HardwareBridgeUpdated(timestamp=now, state=current_state))
                last_state = current_state
                
            await asyncio.sleep(0.05) # 20Hz loop
