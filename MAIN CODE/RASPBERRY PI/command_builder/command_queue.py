"""
command_queue.py
Recon Rover V1 - Command Builder

Bounded priority queue for CommandPackets.
"""

import asyncio
from .command_models import CommandPacket, MotorCommand
from .command_priority import CommandPriority

class CommandQueue:
    """
    Asynchronous, bounded priority queue with duplicate suppression.
    """
    def __init__(self, max_size: int = 50):
        self.queue = asyncio.PriorityQueue()
        self.max_size = max_size
        self._last_motor_action: str = ""

    def put_nowait(self, packet: CommandPacket) -> bool:
        """
        Attempts to enqueue a packet. 
        Returns True if successful, False if dropped due to queue overflow or duplication.
        """
        # Duplicate suppression for MotorCommands
        if isinstance(packet, MotorCommand):
            if packet.action == self._last_motor_action and packet.priority != CommandPriority.EMERGENCY:
                # Dropping identical back-to-back motor command
                return False
            self._last_motor_action = packet.action

        # Overflow handling
        if self.queue.qsize() >= self.max_size:
            if packet.priority == CommandPriority.EMERGENCY:
                # Force room for emergency
                # We can't easily pop the lowest priority from an asyncio.PriorityQueue without emptying it, 
                # but for an unbounded-like queue bounded manually, we can just grab one item to discard.
                try:
                    self.queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            else:
                # Drop non-emergency packet
                return False

        try:
            self.queue.put_nowait(packet)
            return True
        except asyncio.QueueFull:
            return False

    async def get(self) -> CommandPacket:
        """Blocks until a packet is available."""
        return await self.queue.get()

    def task_done(self):
        self.queue.task_done()
        
    def qsize(self) -> int:
        return self.queue.qsize()
