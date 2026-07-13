"""
serial_writer.py
Recon Rover V1 - Serial Communication Manager

Subscribes to CommandPacketReady, serializes packets to JSON, adds CRC/framing, and sends.
"""

import json
import zlib
import asyncio
from logger import Logger
from event_bus import EventBus, CommandPacketReady
from .serial_connection import SerialConnection
from .serial_statistics import SerialStatistics

class SerialWriter:
    def __init__(self, connection: SerialConnection, event_bus: EventBus, stats: SerialStatistics):
        self.connection = connection
        self.event_bus = event_bus
        self.stats = stats
        self.log = Logger.get("SerialWriter")
        self._running = False
        self._queue = asyncio.Queue(maxsize=100)

    def start(self):
        if not self._running:
            self.event_bus.subscribe(CommandPacketReady, self._on_command_ready)
            self._running = True
            asyncio.create_task(self._write_loop())

    def stop(self):
        self._running = False

    async def _on_command_ready(self, event: CommandPacketReady):
        if not self._running:
            return
        try:
            self._queue.put_nowait(event.packet)
        except asyncio.QueueFull:
            self.stats.record_dropped()

    async def _write_loop(self):
        while self._running:
            try:
                packet = await self._queue.get()
                
                if not self.connection.is_open():
                    self.stats.record_dropped()
                    self._queue.task_done()
                    continue
                    
                frame = self._serialize(packet)
                if frame:
                    success = await self.connection.write(frame)
                    if success:
                        self.stats.record_tx(len(frame))
                    else:
                        self.stats.record_dropped()
                        
                self._queue.task_done()
            except Exception as e:
                self.log.error(f"Writer loop error: {e}")
                await asyncio.sleep(0.1)

    def _serialize(self, packet) -> bytes:
        """
        Converts dataclass -> dict -> JSON -> bytes -> CRC -> Framed bytes.
        """
        try:
            # We construct a simple dict depending on the packet fields
            # For simplicity, convert the dataclass __dict__ filtering out priority/timestamp
            payload_dict = {k: v for k, v in packet.__dict__.items() if k not in ['priority', 'timestamp_ms']}
            
            json_str = json.dumps(payload_dict)
            json_bytes = json_str.encode('utf-8')
            
            crc = format(zlib.crc32(json_bytes) & 0xFFFFFFFF, '08x').encode('ascii')
            
            return b'^' + crc + b'|' + json_bytes + b'$'
        except Exception as e:
            self.log.error(f"Serialization error: {e}")
            return b""
