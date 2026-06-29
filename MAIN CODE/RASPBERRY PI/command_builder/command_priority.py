"""
command_priority.py
Recon Rover V1 - Command Builder

Defines deterministic priorities for command packets.
"""

from enum import IntEnum

class CommandPriority(IntEnum):
    """
    Lower integer value = Higher priority in the queue.
    """
    EMERGENCY = 0
    MOTOR = 1
    SERVO = 2
    OLED = 3
    LED = 4
    DIAGNOSTICS = 5
