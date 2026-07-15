"""
Telemetry Manager Module
Recon Rover V2 - Phase 2.3

The central orchestrator for incoming telemetry.
Subscribes to raw Serial/WiFi packet events, decodes them via TelemetryDecoder,
updates tracking statistics, and broadcasts strictly-typed Events to the system.
"""

import sys
import os
import asyncio
from typing import Any

from .telemetry_events import SerialPacketReceived, HeartbeatUpdated, SensorUpdated, TelemetryHealthUpdated
from .telemetry_decoder import TelemetryDecoder
from .telemetry_health import TelemetryHealth

# Dynamic path resolution for SHARED definitions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from packets import HeartbeatPacket, SensorTelemetry
except ImportError:
    pass


class TelemetryManager:
    """
    Manages the translation of physical byte streams into cognitive EventBus objects.
    """
    
    def __init__(self, event_bus: Any):
        """
        Initializes the Telemetry Manager.
        """
        self._bus = event_bus
        self._health = TelemetryHealth()
        
        # Subscribe to incoming raw byte streams (e.g. from a Serial driver not implemented yet)
        self._bus.subscribe(SerialPacketReceived, self._handle_raw_packet)
        
        # We could also launch an asyncio task to periodically broadcast health
        # self._health_task = asyncio.create_task(self._broadcast_health_loop())
        
    async def _handle_raw_packet(self, event: SerialPacketReceived) -> None:
        """
        Processes an incoming byte array.
        """
        raw_bytes = event.raw_data
        
        # 1. Decode Header
        header = TelemetryDecoder.decode_header(raw_bytes)
        if not header:
            # Invalid header, drop silently or log
            return
            
        # 2. Update Health Statistics (Sequence numbers, latency)
        self._health.record_packet(header.sequence_num, event.timestamp_ms)
        
        # 3. Decode Payload
        payload = TelemetryDecoder.decode_payload(header, raw_bytes)
        if not payload:
            return
            
        # 4. Route Payload to specific strongly-typed EventBus objects
        if isinstance(payload, HeartbeatPacket):
            self._health.record_heartbeat()
            self._bus.publish(HeartbeatUpdated(
                system_state=payload.system_state,
                operating_mode=payload.operating_mode,
                mission_mode=payload.mission_mode,
                battery_v=payload.battery_v,
                uptime_ms=payload.uptime_ms
            ))
            
        elif isinstance(payload, SensorTelemetry):
            self._bus.publish(SensorUpdated(
                sensor_type=payload.sensor_type,
                reading_1=payload.reading_1,
                reading_2=payload.reading_2,
                reading_3=payload.reading_3,
                timestamp_ms=event.timestamp_ms
            ))
            
    async def _broadcast_health_loop(self):
        """
        Periodically publishes TelemetryHealthUpdated.
        """
        while True:
            await asyncio.sleep(1.0) # 1Hz broadcast
            stats = self._health.get_statistics()
            self._bus.publish(TelemetryHealthUpdated(
                packet_loss_pct=stats['packet_loss_pct'],
                latency_ms=stats['latency_ms'],
                packets_per_second=stats['packets_per_second'],
                is_healthy=stats['is_healthy']
            ))
