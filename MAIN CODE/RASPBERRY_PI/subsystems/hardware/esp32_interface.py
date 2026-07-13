"""
esp32_interface.py
Recon Rover V1 - Hardware Interface

The main software bridge bridging the EventBus to the physical serial port.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, ExecutionRequest, EmergencyStop,
    TelemetryReceived, SensorStateUpdated, ESP32Connected, ESP32Disconnected,
    HeartbeatTimeout, HardwareHealthUpdated, MissionUpdated
)

from .serial_transport import SerialTransport
from .connection_manager import ConnectionManager
from .reconnect_manager import ReconnectManager
from .heartbeat_monitor import HeartbeatMonitor
from .command_translator import CommandTranslator
from .telemetry_receiver import TelemetryReceiver
from .hardware_health import HardwareHealth
from .hardware_statistics import HardwareStatistics

class ESP32Interface(BaseModule):
    def __init__(self, event_bus: EventBus, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        super().__init__()
        self.event_bus = event_bus
        
        self.transport = SerialTransport(port, baudrate)
        self.conn_manager = ConnectionManager(self.event_bus, self.transport)
        self.reconnect_manager = ReconnectManager(self.conn_manager)
        
        self.heartbeat = HeartbeatMonitor(self.event_bus)
        self.translator = CommandTranslator()
        self.receiver = TelemetryReceiver(self.event_bus)
        
        self.health_tracker = HardwareHealth()
        self.stats = HardwareStatistics()
        
        self._running = False
        self._rx_task = None
        self._hb_task = None
        
        self._subscribe_events()

    def _subscribe_events(self):
        self.event_bus.subscribe(ExecutionRequest, self._on_execution_request)
        self.event_bus.subscribe(EmergencyStop, self._on_emergency_stop)
        
    async def initialize(self):
        self.log.info("ESP32Interface (Phase 5.9) initialized.")

    async def start(self):
        self._running = True
        self.reconnect_manager.trigger_reconnect()
        self._rx_task = asyncio.create_task(self._rx_loop())
        self._hb_task = asyncio.create_task(self._heartbeat_loop())
        self.log.info("ESP32Interface started.")

    async def stop(self):
        self._running = False
        self.reconnect_manager.stop()
        if self._rx_task:
            self._rx_task.cancel()
        if self._hb_task:
            self._hb_task.cancel()
        await self.conn_manager.handle_disconnect("Graceful Shutdown")
        self.log.info("ESP32Interface stopped.")

    def health(self) -> str:
        return self.health_tracker.status

    # --- TX Flow ---
    async def _on_execution_request(self, event: ExecutionRequest):
        packet = self.translator.translate_execution_request(event.action)
        success = await self.transport.write(packet)
        if success:
            self.stats.record_tx(len(packet))
        else:
            self.health_tracker.record_drop()

    async def _on_emergency_stop(self, event: EmergencyStop):
        packet = self.translator.translate_emergency_stop()
        # Fire-and-forget, bypass queues
        success = await self.transport.write(packet)
        if success:
            self.stats.record_tx(len(packet))
        else:
            self.health_tracker.record_drop()

    # --- RX Flow ---
    async def _rx_loop(self):
        while self._running:
            if not self.conn_manager.connected:
                await asyncio.sleep(0.1)
                continue
                
            try:
                raw_bytes = await self.transport.read_line()
                if raw_bytes:
                    self.stats.record_rx(len(raw_bytes))
                    self.heartbeat.record_ack()
                    self.receiver.process_raw_packet(raw_bytes)
            except Exception as e:
                self.log.error(f"Serial read error: {e}")
                await self.conn_manager.handle_disconnect("Serial Error")
                self.health_tracker.set_disconnected()
                self.reconnect_manager.trigger_reconnect()

    # --- Heartbeat Flow ---
    async def _heartbeat_loop(self):
        while self._running:
            if self.conn_manager.connected:
                # 1. Send Ping
                ping = b'{"type":"command","command":"PING"}\n'
                await self.transport.write(ping)
                
                # 2. Check timeout on previous ACKs
                if not self.heartbeat.check_health():
                    self.log.warning("Heartbeat Timeout! Triggering reconnect.")
                    await self.conn_manager.handle_disconnect("Heartbeat Timeout")
                    self.health_tracker.set_disconnected()
                    self.reconnect_manager.trigger_reconnect()
                    
            await asyncio.sleep(1.0)
