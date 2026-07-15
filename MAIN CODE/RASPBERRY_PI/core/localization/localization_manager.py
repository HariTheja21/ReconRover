"""
Localization Manager Module
Recon Rover V2 - Phase 3.3
"""
import asyncio
import time
from typing import Any
from .localization_engine import LocalizationEngine
from .localization_health import LocalizationHealth
from .localization_statistics import LocalizationStatistics
from .localization_events import RobotPoseUpdated, VelocityUpdated, LocalizationUpdated

try:
    from core.event_bus import Event
    from core.fusion.fusion_events import FusedDistance
    from core.sensors.sensor_events import IMUUpdated
except ImportError:
    class Event: pass
    class FusedDistance: pass
    class IMUUpdated: pass

class LocalizationManager:
    """The central daemon for the Localization Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.engine = LocalizationEngine()
        self.health = LocalizationHealth(self._bus)
        self.stats = LocalizationStatistics()
        
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
        self._bus.subscribe(IMUUpdated, self._handle_imu)
        # Using FusedDistance for simplistic relative velocity heuristic
        self._bus.subscribe(FusedDistance, self._handle_fused_distance)
        
    async def _handle_imu(self, event: Any):
        pitch = getattr(event, "pitch", 0.0)
        roll = getattr(event, "roll", 0.0)
        yaw = getattr(event, "yaw", 0.0)
        self.engine.orientation.update_from_imu(pitch, roll, yaw)
        
    async def _handle_fused_distance(self, event: Any):
        dist = getattr(event, "distance_cm", 0.0)
        self.engine.velocity.update_distance(dist)
        
    async def _publish_loop(self):
        """Runs the localization pipeline at 20Hz."""
        while self._running:
            x, y, theta, conf, lin_vel, ang_vel, hist_size = self.engine.tick()
            
            self._bus.publish(RobotPoseUpdated(
                timestamp=time.time(),
                x=x,
                y=y,
                theta=theta,
                confidence=conf
            ))
            
            self._bus.publish(VelocityUpdated(
                timestamp=time.time(),
                linear_velocity=lin_vel,
                angular_velocity=ang_vel
            ))
            
            self._bus.publish(LocalizationUpdated(
                timestamp=time.time(),
                pose_history_size=hist_size
            ))
            
            self.stats.increment()
            await asyncio.sleep(0.05) # 20Hz cycle for localization math
