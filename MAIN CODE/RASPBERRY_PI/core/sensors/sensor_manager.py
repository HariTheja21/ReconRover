"""
Sensor Manager
Recon Rover V2 - Phase 2.9
"""
from typing import Any
import asyncio
from .sensor_router import SensorRouter
from .sensor_statistics import SensorStatistics
from .sensor_health import SensorHealth
from .sensor_events import TelemetryPacket

try:
    from core.managers.config_events import ConfigurationUpdated
except ImportError:
    class ConfigurationUpdated: pass

class SensorManager:
    """Master node for the Sensor Subsystem."""
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = SensorStatistics()
        self.health = SensorHealth(self._bus, self.stats)
        self.router = SensorRouter(self._bus)
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        
    def stop(self):
        self.health.stop()
        
    def _subscribe_events(self):
        self._bus.subscribe(TelemetryPacket, self._handle_telemetry)
        self._bus.subscribe(ConfigurationUpdated, self._handle_config_update)
        
    async def _handle_telemetry(self, event: Any):
        try:
            self.router.route_packet(event.sensor_type, event.binary_payload)
            self.stats.add_packet()
        except Exception as e:
            print(f"SENSOR ROUTER ERROR: {e}")
            self.health.is_healthy = False
            self.health.status_flags["router"] = False
            
    async def _handle_config_update(self, event: Any):
        """Cascades new sensor limits/offsets."""
        if hasattr(event, 'current_config'):
            self.router.update_config(event.current_config)
