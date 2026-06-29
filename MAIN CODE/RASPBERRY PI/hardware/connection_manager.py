"""
connection_manager.py
Recon Rover V1 - Hardware Interface

Maintains connection state and publishes connection lifecycle events.
"""

from event_bus import EventBus, ESP32Connected, ESP32Disconnected
from .serial_transport import SerialTransport

class ConnectionManager:
    def __init__(self, event_bus: EventBus, transport: SerialTransport):
        self.event_bus = event_bus
        self.transport = transport
        self.connected = False
        
    async def attempt_connect(self) -> bool:
        success = await self.transport.connect()
        if success and not self.connected:
            self.connected = True
            self.event_bus.publish(ESP32Connected(port=self.transport.port))
        return success
        
    async def handle_disconnect(self, reason: str):
        if self.connected:
            self.connected = False
            await self.transport.disconnect()
            self.event_bus.publish(ESP32Disconnected(reason=reason))
