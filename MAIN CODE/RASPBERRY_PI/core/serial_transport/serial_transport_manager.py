"""
Serial Transport Manager Module
Recon Rover V2 - Phase 4.3
"""
import asyncio
import time
from typing import Any

from .serial_transport_engine import SerialTransportEngine
from .packet_health import PacketHealth
from .packet_statistics import PacketStatistics
from .serial_events import (SerialPacketSent, SerialPacketReceived, 
                            SerialConnected, SerialDisconnected)

try:
    from core.event_bus import Event
    from core.hardware_bridge.hardware_bridge_events import HardwareCommandPacket, HardwareStopPacket
except ImportError:
    class Event: pass
    class HardwareCommandPacket: pass
    class HardwareStopPacket: pass

class SerialTransportManager:
    """Daemon for the UART Serial Transport Layer."""
    def __init__(self, event_bus: Any, port: str = "/dev/serial0", baudrate: int = 115200):
        self._bus = event_bus
        self.stats = PacketStatistics()
        self.engine = SerialTransportEngine(self.stats, port, baudrate)
        self.health = PacketHealth(self._bus)
        
        self._running = False
        self._loop_task = None
        self._was_connected = False
        
        self._subscribe_events()
        
    def start(self):
        self.health.start()
        self._running = True
        self._loop_task = asyncio.create_task(self._transport_loop())
        
    def stop(self):
        self._running = False
        self.health.stop()
        self.engine.disconnect()
        if self._loop_task:
            self._loop_task.cancel()
            
    def _subscribe_events(self):
        self._bus.subscribe(HardwareCommandPacket, self._handle_cmd_packet)
        self._bus.subscribe(HardwareStopPacket, self._handle_stop_packet)
        
    async def _handle_cmd_packet(self, event: Any):
        packet = getattr(event, "packet_data", None)
        if packet:
            self.engine.queue_outgoing(packet, force_front=False)
            
    async def _handle_stop_packet(self, event: Any):
        packet = getattr(event, "packet_data", None)
        if packet:
            # E-Stops jump to the front of the queue
            self.engine.queue_outgoing(packet, force_front=True)
            
    async def _transport_loop(self):
        """Runs the high-speed UART TX/RX loop at ~50Hz (0.02s)."""
        while self._running:
            is_conn = self.engine.is_connected()
            
            # Handle Connection State Changes
            if is_conn and not self._was_connected:
                self.health.set_connected(True)
                self._bus.publish(SerialConnected(time.time(), self.engine.serial.port, self.engine.serial.baudrate))
                self._was_connected = True
            elif not is_conn and self._was_connected:
                self.health.set_connected(False)
                self._bus.publish(SerialDisconnected(time.time(), "Connection Lost"))
                self._was_connected = False
                
            # Attempt reconnect if down
            if not is_conn:
                self.engine.connect()
                await asyncio.sleep(1.0) # Backoff
                continue
                
            # RX Processing
            incoming_packets = self.engine.process_rx()
            for p in incoming_packets:
                self._bus.publish(SerialPacketReceived(time.time(), p))
                
            # TX Processing (Send one per tick to prevent buffer bloat)
            sent = self.engine.process_tx()
            if sent:
                # We don't have sequence number available here easily without parsing the raw packet again,
                # but we emit the event. In a full system, we could parse it or pass it alongside the bytes.
                self._bus.publish(SerialPacketSent(time.time(), 0, len(self.engine.sender._queue.queue) if hasattr(self.engine.sender._queue, 'queue') else 0))
                
            await asyncio.sleep(0.02) # ~50Hz polling loop
