"""
Serial Manager Module
Recon Rover V2 - Phase 2.4

The central orchestrator for the physical layer.
Initializes the port manager, statistics, health, reader, writer, and watchdog.
"""

import asyncio
from typing import Any

from .serial_port_manager import SerialPortManager
from .serial_statistics import SerialStatistics
from .serial_health import SerialHealth
from .serial_watchdog import SerialWatchdog
from .serial_packet_reader import SerialPacketReader
from .serial_packet_writer import SerialPacketWriter
from .event_bridge import EventBridge
from .hal_events import SerialConnected, SerialDisconnected

class SerialManager:
    """
    Manages the lifecycle of all HAL components and the physical connection.
    """
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        
        self.port_manager = SerialPortManager()
        self.stats = SerialStatistics()
        self.health = SerialHealth(self._bus, self.stats)
        self.watchdog = SerialWatchdog(self._bus)
        
        self.writer = SerialPacketWriter(self.stats)
        self.event_bridge = EventBridge(self._bus, self.writer)
        self.reader = SerialPacketReader(self.stats, self._on_packet_extracted)
        
        self._running = False
        self._monitor_task = None
        
    def _on_packet_extracted(self, raw_bytes: bytes):
        """Callback from SerialPacketReader when a valid packet is aligned."""
        self.watchdog.ping()
        self.event_bridge.on_raw_packet_received(raw_bytes)
        
    async def start(self):
        """Starts the Serial Manager and background monitoring loop."""
        self._running = True
        self._monitor_task = asyncio.create_task(self._connection_monitor_loop())
        
    async def stop(self):
        """Stops all HAL components."""
        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
        self._disconnect()
        
    def _connect(self):
        """Attempts to open port and start IO tasks."""
        if self.port_manager.connect():
            self.health.set_connected_state(True)
            self.reader.start(self.port_manager.get_connection())
            self.writer.start(self.port_manager.get_connection())
            
            self._bus.publish(SerialConnected(
                port=self.port_manager.active_port_name,
                baudrate=self.port_manager.baudrate
            ))
            return True
        return False
        
    def _disconnect(self):
        """Stops IO tasks and closes port."""
        self.reader.stop()
        self.writer.stop()
        
        was_connected = self.health.is_connected
        self.health.set_connected_state(False)
        self.port_manager.disconnect()
        
        if was_connected:
            self._bus.publish(SerialDisconnected(
                port="UNKNOWN",
                reason="Disconnected by manager"
            ))
            
    async def _connection_monitor_loop(self):
        """
        Background loop handling auto-connect and watchdog timeouts.
        """
        while self._running:
            try:
                if not self.health.is_connected:
                    self._connect()
                else:
                    if self.watchdog.check():
                        # Timeout triggered, force reconnect
                        self._disconnect()
                        
                self.health.broadcast_health()
                await asyncio.sleep(1.0)
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(1.0)
