"""
command_models.py
Recon Rover V1 - Command Builder

Dataclasses representing structured protocol packets.
"""

from dataclasses import dataclass, field
from .command_priority import CommandPriority
import time

@dataclass(order=True)
class CommandPacket:
    """
    Base class for all commands. Sortable by priority.
    """
    priority: CommandPriority
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000), compare=True)
    command_type: str = field(default="sys", compare=False)

@dataclass(order=True)
class MotorCommand(CommandPacket):
    command_type: str = field(default="mot", compare=False)
    action: str = field(default="stop", compare=False) # e.g., "fwd", "rev", "left", "right", "stop"
    speed: int = field(default=0, compare=False)       # 0 to 100

@dataclass(order=True)
class ServoCommand(CommandPacket):
    command_type: str = field(default="srv", compare=False)
    pan_angle: int = field(default=90, compare=False)
    tilt_angle: int = field(default=90, compare=False)

@dataclass(order=True)
class LEDCommand(CommandPacket):
    command_type: str = field(default="led", compare=False)
    mode: str = field(default="solid", compare=False)
    r: int = field(default=0, compare=False)
    g: int = field(default=0, compare=False)
    b: int = field(default=0, compare=False)

@dataclass(order=True)
class OLEDCommand(CommandPacket):
    command_type: str = field(default="old", compare=False)
    line1: str = field(default="", compare=False)
    line2: str = field(default="", compare=False)
    line3: str = field(default="", compare=False)
    line4: str = field(default="", compare=False)

@dataclass(order=True)
class SystemCommand(CommandPacket):
    command_type: str = field(default="sys", compare=False)
    action: str = field(default="ping", compare=False)
