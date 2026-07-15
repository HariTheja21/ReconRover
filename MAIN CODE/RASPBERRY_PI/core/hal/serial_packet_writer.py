"""
Serial Packet Writer Module
Recon Rover V2 - Phase 2.4

Asynchronous non-blocking queue to dispatch outgoing bytes to the serial port.
"""

import asyncio
from typing import Any
from .serial_statistics import SerialStatistics

class SerialPacketWriter:
    """
    Manages the outbound physical buffer queue to prevent blocking the event loop
    when writing to a potentially slow serial port.
    """
    
    def __init__(self, stats: SerialStatistics):
        self._stats = stats
        self._queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._task = None
        self._connection = None
        
    def start(self, connection: Any):
        """Starts the async write loop."""
        if not connection:
            return
        self._connection = connection
        self._running = True
        self._task = asyncio.create_task(self._write_loop())
        
    def stop(self):
        """Stops the write loop."""
        self._running = False
        if self._task:
            self._task.cancel()
        self._connection = None
        
    def enqueue(self, raw_bytes: bytes):
        """Adds a byte array to the outbound queue."""
        if self._running:
            try:
                self._queue.put_nowait(raw_bytes)
            except asyncio.QueueFull:
                self._stats.add_dropped()
                
    async def _write_loop(self):
        """Continuously pops from the queue and writes to the physical port."""
        while self._running:
            try:
                data = await self._queue.get()
                
                if self._connection == "MOCK_CONNECTION":
                    self._stats.add_tx(len(data))
                    self._stats.add_valid_tx()
                elif hasattr(self._connection, 'write'):
                    written = self._connection.write(data)
                    # If using standard pyserial, .write might block, but timeout=0 helps.
                    if hasattr(self._connection, 'flush'):
                        self._connection.flush()
                        
                    self._stats.add_tx(written or len(data))
                    self._stats.add_valid_tx()
                    
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception:
                # Disconnect or IO error handling handled by manager
                self._running = False
                break
