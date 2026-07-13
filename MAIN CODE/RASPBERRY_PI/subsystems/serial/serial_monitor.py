"""
serial_monitor.py
Recon Rover V1 - Serial Communication Manager

Continuously monitors the connection state and triggers reconnects.
"""

import asyncio
import time
from logger import Logger
from event_bus import EventBus, SerialConnected, SerialDisconnected, SerialError
from .serial_connection import SerialConnection
from .reconnect_manager import ReconnectManager
from .serial_health import SerialHealth

class SerialMonitor:
    def __init__(self, connection: SerialConnection, event_bus: EventBus, health: SerialHealth, heartbeat_timeout_ms: int = 5000):
        self.connection = connection
        self.event_bus = event_bus
        self.health = health
        self.reconnect_manager = ReconnectManager()
        self.heartbeat_timeout_sec = heartbeat_timeout_ms / 1000.0
        self.log = Logger.get("SerialMonitor")
        self._running = False
        self._task = None

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._monitor_loop())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _monitor_loop(self):
        while self._running:
            try:
                if not self.connection.is_open():
                    self.health.is_connected = False
                    self.event_bus.publish(SerialDisconnected())
                    self.log.warning("Serial disconnected. Attempting reconnect...")
                    
                    if self.connection.connect():
                        self.health.is_connected = True
                        self.reconnect_manager.reset_backoff()
                        self.event_bus.publish(SerialConnected(port=self.connection.port))
                        self.log.info("Serial reconnected successfully.")
                    else:
                        await self.reconnect_manager.wait_before_reconnect()
                        continue
                
                # Check heartbeat timeout
                now = int(time.time() * 1000)
                if (now - self.health.last_heartbeat_ms) > (self.heartbeat_timeout_sec * 1000):
                    if self.health.is_connected:
                        self.log.error("Heartbeat timeout! Forcing connection reset.")
                        self.health.error_state = True
                        self.event_bus.publish(SerialError(reason="Heartbeat Timeout"))
                        self.connection.close() # Force close to trigger reconnect next loop
                
                await asyncio.sleep(1.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Monitor loop error: {e}")
                await asyncio.sleep(1.0)
