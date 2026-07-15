"""
Event Bridge Module
Recon Rover V2 - Phase 2.4

The bi-directional gateway between the physical HAL and the abstract EventBus.
"""

import sys
import os
from typing import Any

# Need to import Phase 2.3 TelemetryEncoder if it exists
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
try:
    from RASPBERRY_PI.core.managers.telemetry_encoder import TelemetryEncoder
    from RASPBERRY_PI.core.managers.telemetry_events import SerialPacketReceived
except ImportError:
    pass

class EventBridge:
    """
    Connects the HAL's SerialPacketReader and SerialPacketWriter to the EventBus.
    """
    
    def __init__(self, event_bus: Any, packet_writer: Any):
        self._bus = event_bus
        self._writer = packet_writer
        
        # In a full implementation, we'd subscribe to specific OutgoingCommandPackets
        # For this phase, we mock the subscription.
        # self._bus.subscribe(OutgoingMotionCommand, self._handle_outgoing_motion)
        
    def on_raw_packet_received(self, raw_bytes: bytes):
        """
        Callback from SerialPacketReader when a fully validated raw packet is extracted.
        Pushes it to the EventBus for the TelemetryManager to decode.
        """
        import time
        # Publish to the EventBus where TelemetryManager from Phase 2.3 is listening
        try:
            self._bus.publish(SerialPacketReceived(
                raw_data=raw_bytes,
                timestamp_ms=int(time.time() * 1000)
            ))
        except NameError:
            pass # Fallback if SerialPacketReceived isn't imported
            
    # async def _handle_outgoing_motion(self, event):
    #     raw = TelemetryEncoder.encode_motion_command(event.command)
    #     self._writer.enqueue(raw)
