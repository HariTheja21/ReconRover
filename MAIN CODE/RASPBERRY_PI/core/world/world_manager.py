"""
World Manager Module
Recon Rover V2 - Phase 3.1
"""
from typing import Any
import asyncio
import time
from .world_database import WorldDatabase
from .world_health import WorldHealth
from .world_statistics import WorldStatistics
from .world_events import RobotStateUpdated, ObstacleMapUpdated, WorldUpdated, LandmarkUpdated

try:
    from core.sensors.sensor_events import (
        BatteryUpdated, IMUUpdated, OrientationUpdated, DistanceUpdated, ObstacleDetected
    )
except ImportError:
    class BatteryUpdated: pass
    class IMUUpdated: pass
    class OrientationUpdated: pass
    class DistanceUpdated: pass
    class ObstacleDetected: pass

class WorldManager:
    """The central daemon for the World Model Engine."""
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.db = WorldDatabase()
        self.health = WorldHealth(self._bus)
        self.stats = WorldStatistics()
        
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
        self._bus.subscribe(BatteryUpdated, self._handle_battery)
        self._bus.subscribe(OrientationUpdated, self._handle_orientation)
        self._bus.subscribe(ObstacleDetected, self._handle_obstacle)
        
    async def _handle_battery(self, event: Any):
        self.db.state.update_battery(event.percentage)
        self.stats.increment()
        
    async def _handle_orientation(self, event: Any):
        self.db.state.update_imu(event.pitch, event.roll, event.yaw)
        self.stats.increment()
        
    async def _handle_obstacle(self, event: Any):
        self.db.obstacles.add_obstacle(event.sensor_id, event.distance_cm, event.threat_level)
        self.stats.increment()
        
    async def _publish_loop(self):
        """Sweeps memory and publishes state at 10Hz."""
        while self._running:
            self.db.sweep_all()
            
            # Robot State
            rs = self.db.state.get_snapshot()
            self._bus.publish(RobotStateUpdated(
                timestamp=rs["timestamp"],
                battery_percentage=rs["battery"],
                pitch=rs["pitch"],
                roll=rs["roll"],
                yaw=rs["yaw"]
            ))
            
            # Obstacles
            active_obs = self.db.obstacles.get_active()
            self._bus.publish(ObstacleMapUpdated(
                timestamp=time.time(),
                active_obstacles=active_obs
            ))
            
            # Global
            self._bus.publish(WorldUpdated(
                timestamp=time.time(),
                entity_count=len(self.db.entities.get_all()),
                obstacle_count=len(active_obs),
                landmark_count=len(self.db.landmarks.get_all())
            ))
            
            await asyncio.sleep(0.1)
