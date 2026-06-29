"""
serial_reader.py
Recon Rover V1 - Serial Communication Manager

Asynchronous reader task that buffers raw bytes, detects frames,
validates CRC, and dispatches JSON payloads to the EventBus.
"""

import asyncio
import zlib
import json
import time
from logger import Logger
from event_bus import EventBus, TelemetryReceived, HealthReceived
from .serial_connection import SerialConnection
from .serial_statistics import SerialStatistics
from .serial_health import SerialHealth

class SerialReader:
    def __init__(self, connection: SerialConnection, event_bus: EventBus, stats: SerialStatistics, health: SerialHealth):
        self.connection = connection
        self.event_bus = event_bus
        self.stats = stats
        self.health = health
        self.log = Logger.get("SerialReader")
        self._running = False
        self._task = None
        self._buffer = b""

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._read_loop())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _read_loop(self):
        while self._running:
            if not self.connection.is_open():
                await asyncio.sleep(0.5)
                continue
                
            chunk = await self.connection.read_chunk(1024)
            if not chunk:
                await asyncio.sleep(0.01)
                continue
                
            self.stats.record_rx(len(chunk))
            self._buffer += chunk
            self._process_buffer()

    def _process_buffer(self):
        """Finds ^ ... $ frames and parses them."""
        while b'^' in self._buffer and b'$' in self._buffer:
            start_idx = self._buffer.find(b'^')
            end_idx = self._buffer.find(b'$', start_idx)
            
            if start_idx == -1 or end_idx == -1:
                break
                
            frame = self._buffer[start_idx:end_idx+1]
            self._buffer = self._buffer[end_idx+1:]
            
            self._parse_frame(frame)

    def _parse_frame(self, frame: bytes):
        """
        Expected format: ^[4-byte CRC]|JSON$
        """
        if len(frame) < 8:
            self.stats.record_dropped()
            return
            
        try:
            # Strip ^ and $
            content = frame[1:-1]
            
            # Split by '|'
            parts = content.split(b'|', 1)
            if len(parts) != 2:
                self.stats.record_dropped()
                return
                
            crc_hex = parts[0].decode('ascii', errors='ignore')
            json_bytes = parts[1]
            
            # Validate CRC
            expected_crc = format(zlib.crc32(json_bytes) & 0xFFFFFFFF, '08x')
            if crc_hex != expected_crc:
                self.stats.record_crc_failure()
                self.log.warning(f"CRC Mismatch! Expected: {expected_crc}, Got: {crc_hex}")
                return
                
            # Parse JSON
            payload = json.loads(json_bytes.decode('utf-8'))
            self._dispatch_payload(payload)
            
        except Exception as e:
            self.stats.record_dropped()
            self.log.debug(f"Frame parsing error: {e}")

    def _dispatch_payload(self, payload: dict):
        # Update heartbeat
        now = int(time.time() * 1000)
        self.health.update_heartbeat(now)
        
        # Telemetry
        if "imu" in payload or "tof" in payload:
            self.event_bus.publish(TelemetryReceived(timestamp_ms=now, data=payload))
        # Health / System
        elif "sys" in payload:
            # Assumed structural mapping for HealthReceived
            pass
