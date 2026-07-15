"""
Serial Packet Reader Module
Recon Rover V2 - Phase 2.4

Asynchronous sliding-window buffer reader that hunts for packet headers
and passes them to the validator.
"""

import asyncio
from typing import Callable, Any
from .serial_packet_validator import SerialPacketValidator
from .serial_statistics import SerialStatistics

class SerialPacketReader:
    """
    Reads from a pyserial-like connection, buffering bytes and extracting valid packets.
    """
    
    def __init__(self, stats: SerialStatistics, on_packet_cb: Callable[[bytes], None]):
        self._stats = stats
        self._on_packet = on_packet_cb
        self._buffer = bytearray()
        self._running = False
        self._task = None
        
    def start(self, connection: Any):
        """Starts the async read loop."""
        if not connection:
            return
        self._running = True
        self._task = asyncio.create_task(self._read_loop(connection))
        
    def stop(self):
        """Stops the read loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            
    async def _read_loop(self, connection: Any):
        """
        Continuously polls the serial connection.
        If using pyserial in non-blocking mode, we yield to the event loop.
        """
        while self._running:
            try:
                # Mock connection handling
                if connection == "MOCK_CONNECTION":
                    await asyncio.sleep(0.1)
                    continue
                    
                if hasattr(connection, 'in_waiting'):
                    waiting = connection.in_waiting
                    if waiting > 0:
                        data = connection.read(waiting)
                        if data:
                            self._stats.add_rx(len(data))
                            self._buffer.extend(data)
                            self._process_buffer()
                    else:
                        await asyncio.sleep(0.01)
                else:
                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            except Exception:
                # Connection dropped or other IO error
                self._running = False
                break
                
    def _process_buffer(self):
        """
        Sliding window search for SYNC_1 and SYNC_2.
        """
        while True:
            # Need at least header size
            if len(self._buffer) < SerialPacketValidator.HEADER_SIZE:
                break
                
            # Find SYNC_1
            sync1_idx = self._buffer.find(SerialPacketValidator.SYNC_1)
            if sync1_idx == -1:
                # No sync1 found, flush buffer
                self._buffer.clear()
                break
                
            if sync1_idx > 0:
                # Discard garbage before SYNC_1
                del self._buffer[:sync1_idx]
                
            # Buffer might be too small again after discarding
            if len(self._buffer) < SerialPacketValidator.HEADER_SIZE:
                break
                
            # Verify SYNC_2
            if self._buffer[1] != SerialPacketValidator.SYNC_2:
                # False positive, discard SYNC_1 and loop again
                del self._buffer[:1]
                continue
                
            # Extract expected payload length from header bytes (offset 9 is length in uint16)
            # Struct format for len is <H at offset 13 (sync1(1) + sync2(1) + ver(1) + src(1) + dest(1) + prio(1) + seq(2) + time(4) + type(1) = 13)
            # Wait, let's verify offset:
            # 1+1+1+1+1+1 = 6
            # seq (2) = 8
            # time (4) = 12
            # type (1) = 13
            # length (2) starts at 13
            # crc (2) starts at 15
            # total 17. Yes, offset 13.
            try:
                import struct
                payload_len = struct.unpack("<H", self._buffer[13:15])[0]
            except struct.error:
                del self._buffer[:1]
                continue
                
            expected_total_len = SerialPacketValidator.HEADER_SIZE + payload_len
            
            if len(self._buffer) < expected_total_len:
                # Wait for more bytes
                break
                
            # We have a full candidate packet
            candidate = bytes(self._buffer[:expected_total_len])
            
            is_valid, reason = SerialPacketValidator.validate_packet(candidate)
            
            if is_valid:
                self._stats.add_valid_rx()
                self._on_packet(candidate)
            else:
                self._stats.add_crc_error()
                # We could log the reason here
                
            # Remove the processed packet from buffer
            del self._buffer[:expected_total_len]
