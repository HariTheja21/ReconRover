"""
command_models.py
Recon Rover V1 - Command Builder

Dataclasses representing structured protocol packets.
"""

from dataclasses import dataclass, field
from .command_priority import CommandPriority
import time

_seq_counter = 0
def next_seq():
    global _seq_counter
    _seq_counter += 1
    return _seq_counter

@dataclass(order=True)
class CommandPacket:
    """
    Base class for all commands. Sortable by priority.
    """
    priority: CommandPriority
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000), compare=True)
    v_maj: int = field(default=1, compare=False)
    seq: int = field(default_factory=next_seq, compare=False)

@dataclass(order=True)
class MotorCommand(CommandPacket):
    mot: dict = field(default_factory=dict, compare=False)

@dataclass(order=True)
class ServoCommand(CommandPacket):
    srv: dict = field(default_factory=dict, compare=False)

@dataclass(order=True)
class LEDCommand(CommandPacket):
    led: dict = field(default_factory=dict, compare=False)

@dataclass(order=True)
class OLEDCommand(CommandPacket):
    eye: dict = field(default_factory=dict, compare=False)

@dataclass(order=True)
class SystemCommand(CommandPacket):
    sys: dict = field(default_factory=lambda: {"action": "ping"}, compare=False)
