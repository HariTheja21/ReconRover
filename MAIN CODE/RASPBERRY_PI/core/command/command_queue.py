"""
Command Queue Module
Recon Rover V2 - Phase 2.5

Wraps asyncio.PriorityQueue to organize OutgoingCommandPackets.
"""

import asyncio
from typing import Tuple, Any

class CommandQueue:
    """
    Priority-based queuing for outgoing packets.
    Uses standard integer comparison (lower number = higher priority).
    """
    
    def __init__(self, max_size: int = 100):
        # We store tuples of (Priority, timestamp, Packet)
        # Priority mapping: CRITICAL = 0, HIGH = 1, NORMAL = 2, LOW = 3
        # Timestamp ensures FIFO for same-priority items.
        self._queue = asyncio.PriorityQueue(maxsize=max_size)
        
    def enqueue(self, packet: Any) -> bool:
        """
        Attempts to add a packet to the queue.
        Returns False if queue is full.
        """
        import time
        
        # Invert priority values so higher enums process faster, or define mapping
        # If PacketPriority.CRITICAL = 3, HIGH = 2, NORMAL = 1, LOW = 0
        # Then we want 0 for CRITICAL in the python queue.
        # queue_prio = 10 - packet.priority
        queue_prio = 10 - getattr(packet, 'priority', 1) 
        
        item = (queue_prio, time.time_ns(), packet)
        try:
            self._queue.put_nowait(item)
            return True
        except asyncio.QueueFull:
            return False
            
    async def get_next(self) -> Any:
        """
        Yields the highest priority packet.
        """
        _, _, packet = await self._queue.get()
        return packet
        
    def task_done(self):
        self._queue.task_done()
        
    @property
    def qsize(self) -> int:
        return self._queue.qsize()
