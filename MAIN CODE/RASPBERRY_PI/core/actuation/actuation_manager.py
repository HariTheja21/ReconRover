"""
Actuation Manager Module
Recon Rover V2 - Phase 2.8

The master orchestrator for the Actuation Node.
"""

from typing import Any
import asyncio
from .hardware_router import HardwareRouter
from .hardware_statistics import HardwareStatistics
from .hardware_health import HardwareHealth
from .actuation_events import MotorCommandRequest # fallback safety

try:
    from core.command.command_events import OutgoingCommandPacket
except ImportError:
    class OutgoingCommandPacket: pass

try:
    from core.managers.safety_events import EmergencyStopActivated
except ImportError:
    class EmergencyStopActivated: pass
    
try:
    from core.managers.config_events import ConfigurationUpdated
except ImportError:
    class ConfigurationUpdated: pass


class ActuationManager:
    """Master node for the Actuation subsystem."""
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = HardwareStatistics()
        self.health = HardwareHealth(self._bus, self.stats)
        self.router = HardwareRouter(self._bus)
        
        self.is_locked = False
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        
    def stop(self):
        self.health.stop()
        
    def _subscribe_events(self):
        self._bus.subscribe(OutgoingCommandPacket, self._handle_outgoing_command)
        self._bus.subscribe(EmergencyStopActivated, self._handle_estop)
        self._bus.subscribe(ConfigurationUpdated, self._handle_config_update)
        
    async def _handle_outgoing_command(self, event: Any):
        """Asynchronously routes packets unless locked."""
        if self.is_locked:
            return
            
        try:
            self.router.route_packet(event.command_type, event.binary_payload)
            self.stats.add_command()
        except Exception as e:
            print(f"ROUTER ERROR: {e}")
            self.health.is_healthy = False
            self.health.status_flags["router"] = False
            
    async def _handle_estop(self, event: Any):
        """Hard locks the router and immediately fires 0 PWM to HAL."""
        self.is_locked = True
        # Safety override - bypass routing logic and blast a halt directly
        self._bus.publish(MotorCommandRequest(left_pwm=0, right_pwm=0, duration_ms=0))
        
    async def _handle_config_update(self, event: Any):
        """Cascades new limits."""
        if hasattr(event, 'current_config'):
            self.router.update_config(event.current_config)
