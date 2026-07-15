"""
Telemetry Encoder Module
Recon Rover V2 - Phase 2.3

Serializes Command and Configuration packets into raw byte streams
for transmission to the hardware layer.
"""

import struct
import sys
import os
import time
from typing import Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from packets import MotionCommand, ServoCommand, MissionPacket, ConfigurationPacket, PacketHeader
    from constants import CommunicationConstants, SystemConstants
    from enums import CommandType, ModuleID, PacketPriority
except ImportError:
    pass

class TelemetryEncoder:
    """
    Encodes outgoing Python dataclasses into binary packets.
    """
    
    # Header format: sync1, sync2, ver, src, dest, prio, seq, time, type, len, crc
    HEADER_FORMAT = "<BBBBBBHIBHH"
    
    # Payload formats
    # Motion: left(2-int), right(2-int), duration(2-uint) -> hhH (6 bytes)
    MOTION_FORMAT = "<hhH"
    
    # Mission: mission_mode(1), command_type(1), waypoint_count(2-uint) -> BBH (4 bytes)
    MISSION_FORMAT = "<BBH"
    
    _sequence_counter = 0
    
    @classmethod
    def _build_header_bytes(cls, dest: int, prio: int, p_type: int, p_len: int) -> bytearray:
        cls._sequence_counter = (cls._sequence_counter + 1) % 65535
        timestamp = int(time.time() * 1000) & 0xFFFFFFFF
        
        # We start with a dummy CRC of 0
        hdr = struct.pack(
            cls.HEADER_FORMAT,
            getattr(CommunicationConstants, 'SYNC_BYTE_1', 0xAA),
            getattr(CommunicationConstants, 'SYNC_BYTE_2', 0x55),
            getattr(SystemConstants, 'PROTOCOL_VERSION', 2),
            getattr(ModuleID, 'RPI_COMMAND_BUILDER', 16),
            dest,
            prio,
            cls._sequence_counter,
            timestamp,
            p_type,
            p_len,
            0 # CRC placeholder
        )
        # In a full implementation, we'd calculate CRC here and re-pack.
        return bytearray(hdr)

    @classmethod
    def encode_motion_command(cls, cmd: MotionCommand) -> bytes:
        payload = struct.pack(cls.MOTION_FORMAT, cmd.left_pwm, cmd.right_pwm, cmd.duration_ms)
        hdr = cls._build_header_bytes(
            dest=getattr(ModuleID, 'ESP32_ROVER_CORE', 1),
            prio=getattr(PacketPriority, 'HIGH', 2),
            p_type=getattr(CommandType, 'MOTION', 10),
            p_len=len(payload)
        )
        return bytes(hdr + payload)

    @classmethod
    def encode_mission_command(cls, cmd: MissionPacket) -> bytes:
        payload = struct.pack(cls.MISSION_FORMAT, cmd.mission_mode, cmd.command_type, cmd.waypoint_count)
        hdr = cls._build_header_bytes(
            dest=getattr(ModuleID, 'ESP32_ROVER_CORE', 1),
            prio=getattr(PacketPriority, 'NORMAL', 1),
            p_type=getattr(CommandType, 'MISSION', 17),
            p_len=len(payload)
        )
        return bytes(hdr + payload)
