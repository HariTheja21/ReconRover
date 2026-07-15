"""
Command Encoder Module
Recon Rover V2 - Phase 2.5

Translates validated high-level intents into binary arrays leveraging the Shared 
Definitions Framework, ensuring structural integrity of outgoing physical packets.
"""

import sys
import os
import struct
import time
from typing import Any

# Use shared definitions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from constants import CommunicationConstants, SystemConstants
    from enums import CommandType, ModuleID, PacketPriority
    from packets import MotionCommand, MissionPacket # And others as defined
except ImportError:
    class CommunicationConstants: SYNC_BYTE_1 = 0xAA; SYNC_BYTE_2 = 0x55
    class SystemConstants: PROTOCOL_VERSION = 2
    class CommandType: MOTION = 10; MISSION = 17; STOP = 11; MODE = 12
    class ModuleID: RPI_COMMAND_BUILDER = 16; ESP32_ROVER_CORE = 1
    class PacketPriority: CRITICAL = 3; HIGH = 2; NORMAL = 1; LOW = 0
    
from .command_events import (
    MoveIntent, StopIntent, ServoIntent, ModeChangeIntent, MissionChangeIntent, 
    EmergencyStopIntent, OutgoingCommandPacket
)


class CommandEncoder:
    """
    Centralized serialization engine for physical packets.
    """
    
    HEADER_FORMAT = "<BBBBBBHIBHH"
    _sequence = 0
    
    @classmethod
    def _build_binary(cls, dest: int, prio: int, p_type: int, payload: bytes) -> bytes:
        """Constructs the full packet including header."""
        cls._sequence = (cls._sequence + 1) % 65535
        timestamp = int(time.time() * 1000) & 0xFFFFFFFF
        
        hdr = struct.pack(
            cls.HEADER_FORMAT,
            getattr(CommunicationConstants, 'SYNC_BYTE_1', 0xAA),
            getattr(CommunicationConstants, 'SYNC_BYTE_2', 0x55),
            getattr(SystemConstants, 'PROTOCOL_VERSION', 2),
            getattr(ModuleID, 'RPI_COMMAND_BUILDER', 16),
            dest,
            prio,
            cls._sequence,
            timestamp,
            p_type,
            len(payload),
            0 # CRC Placeholder
        )
        return hdr + payload

    @classmethod
    def encode(cls, intent: Any, target_priority: int) -> OutgoingCommandPacket:
        """
        Routes and encodes the intent to a binary OutgoingCommandPacket.
        """
        if isinstance(intent, MoveIntent):
            payload = struct.pack("<hhH", intent.left_pwm, intent.right_pwm, intent.duration_ms)
            p_type = getattr(CommandType, 'MOTION', 10)
            
        elif isinstance(intent, StopIntent):
            payload = struct.pack("<B", 1) # Simple stop flag
            p_type = getattr(CommandType, 'STOP', 11)
            
        elif isinstance(intent, EmergencyStopIntent):
            payload = struct.pack("<B", 99) # E-Stop flag
            p_type = getattr(CommandType, 'STOP', 11)
            
        elif isinstance(intent, MissionChangeIntent):
            payload = struct.pack("<BBH", intent.mission_mode, intent.command_type, intent.waypoint_count)
            p_type = getattr(CommandType, 'MISSION', 17)
            
        elif isinstance(intent, ModeChangeIntent):
            payload = struct.pack("<B", intent.mode)
            p_type = getattr(CommandType, 'MODE', 12)
            
        else:
            # Fallback for unmapped intents (e.g. Servo)
            payload = b"\x00"
            p_type = 255
            
        binary = cls._build_binary(
            dest=getattr(ModuleID, 'ESP32_ROVER_CORE', 1),
            prio=target_priority,
            p_type=p_type,
            payload=payload
        )
        
        return OutgoingCommandPacket(
            binary_payload=binary,
            priority=target_priority,
            command_type=p_type
        )
