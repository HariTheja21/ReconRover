"""
Fusion Manager Module
Recon Rover V2 - Phase 3.2
"""
import asyncio
import time
from typing import Any
from .fusion_engine import FusionEngine
from .fusion_health import FusionHealth
from .fusion_statistics import FusionStatistics
from .fusion_events import (
    FusedObstacle, FusedDistance, FusedOrientation, 
    SensorConfidenceUpdated, EnvironmentUpdated
)

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

class FusionManager:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.engine = FusionEngine()
        self.health = FusionHealth(self._bus)
        self.stats = FusionStatistics()
        
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
        self._bus.subscribe(DistanceUpdated, self._handle_distance)
        self._bus.subscribe(ObstacleDetected, self._handle_obstacle)
        
    async def _handle_distance(self, event: Any):
        # We assume event has sensor_id and distance_cm
        sid = getattr(event, "sensor_id", "UNKNOWN")
        dist = getattr(event, "distance_cm", 0.0)
        self.engine.state.update_observation(sid, "distance", dist)
        
    async def _handle_obstacle(self, event: Any):
        sid = getattr(event, "sensor_id", "UNKNOWN")
        dist = getattr(event, "distance_cm", 0.0)
        self.engine.state.update_observation(sid, "distance", dist)
        
    async def _publish_loop(self):
        while self._running:
            # Fuse distances
            dist_val, dist_conf, used, outliers = self.engine.process_category("distance")
            
            if dist_val is not None:
                self._bus.publish(FusedDistance(
                    timestamp=time.time(),
                    distance_cm=dist_val,
                    confidence=dist_conf,
                    contributing_sensors=used
                ))
                self.stats.increment_fused()
                
                # Also publish a fused obstacle if it's close enough (e.g., < 50cm)
                if dist_val < 50.0:
                    self._bus.publish(FusedObstacle(
                        timestamp=time.time(),
                        distance_cm=dist_val,
                        threat_level="WARNING" if dist_val > 20 else "CRITICAL",
                        confidence=dist_conf,
                        contributing_sensors=used
                    ))
                    
            for out in outliers:
                self.stats.increment_conflicts()
                # Optionally publish confidence update
                c = self.engine.confidence.get_confidence(out)
                self._bus.publish(SensorConfidenceUpdated(
                    timestamp=time.time(),
                    sensor_id=out,
                    confidence=c,
                    reason="Contradictory consensus"
                ))
                
            self._bus.publish(EnvironmentUpdated(
                timestamp=time.time(),
                active_fusions=1 if dist_val is not None else 0
            ))
            
            await asyncio.sleep(0.1) # 10Hz fusion output
