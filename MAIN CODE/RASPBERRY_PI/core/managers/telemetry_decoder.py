"""
Telemetry Decoder Module
Recon Rover V2 - Phase 2.3

Deserializes raw byte streams into Python dataclasses utilizing the
Shared Definitions Framework schemas.
"""

import struct
import sys
import os
from typing import Tuple, Any, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from packets import PacketHeader, HeartbeatPacket, SensorTelemetry
    from constants import CommunicationConstants
    from enums import TelemetryType
except ImportError:
    pass

class TelemetryDecoder:
    """
    Decodes incoming binary telemetry from the ESP32.
    """
    
    # 17 bytes per our Phase 2.1 design: 
    # sync1(1), sync2(1), ver(1), src(1), dest(1), prio(1), seq(2), time(4), type(1), len(2), crc(2)
    # Format: <BBBBBBHIBHH
    HEADER_FORMAT = "<BBBBBBHIBHH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    
    # Payload Formats
    # Heartbeat: sys(1), op(1), miss(1), batt(4-float), uptime(4-uint) -> BBBfI (11 bytes)
    HEARTBEAT_FORMAT = "<BBBfI"
    
    # Sensor: type(1), r1(4f), r2(4f), r3(4f) -> Bfff (13 bytes)
    SENSOR_FORMAT = "<Bfff"

    @classmethod
    def decode_header(cls, raw_bytes: bytes) -> Optional[PacketHeader]:
        """
        Attempts to unpack the packet header.
        """
        if len(raw_bytes) < cls.HEADER_SIZE:
            return None
            
        try:
            unpacked = struct.unpack(cls.HEADER_FORMAT, raw_bytes[:cls.HEADER_SIZE])
            hdr = PacketHeader(
                sync_1=unpacked[0],
                sync_2=unpacked[1],
                protocol_version=unpacked[2],
                source_module=unpacked[3],
                dest_module=unpacked[4],
                priority=unpacked[5],
                sequence_num=unpacked[6],
                timestamp_ms=unpacked[7],
                payload_type=unpacked[8],
                payload_length=unpacked[9],
                header_crc=unpacked[10]
            )
            
            # Basic validation
            if hdr.sync_1 != getattr(CommunicationConstants, 'SYNC_BYTE_1', 0xAA) or \
               hdr.sync_2 != getattr(CommunicationConstants, 'SYNC_BYTE_2', 0x55):
                return None
                
            return hdr
        except struct.error:
            return None

    @classmethod
    def decode_payload(cls, header: PacketHeader, raw_bytes: bytes) -> Optional[Any]:
        """
        Unpacks the payload portion based on the header's payload_type.
        """
        expected_total_len = cls.HEADER_SIZE + header.payload_length
        if len(raw_bytes) < expected_total_len:
            return None # Incomplete packet
            
        payload_bytes = raw_bytes[cls.HEADER_SIZE:expected_total_len]
        
        try:
            if header.payload_type == getattr(TelemetryType, 'HEARTBEAT', 20):
                data = struct.unpack(cls.HEARTBEAT_FORMAT, payload_bytes)
                return HeartbeatPacket(
                    system_state=data[0],
                    operating_mode=data[1],
                    mission_mode=data[2],
                    battery_v=data[3],
                    uptime_ms=data[4]
                )
                
            elif header.payload_type == getattr(TelemetryType, 'IMU', 23) or \
                 header.payload_type == getattr(TelemetryType, 'DISTANCE', 24):
                data = struct.unpack(cls.SENSOR_FORMAT, payload_bytes)
                return SensorTelemetry(
                    sensor_type=data[0],
                    reading_1=data[1],
                    reading_2=data[2],
                    reading_3=data[3]
                )
                
            # Add other payload decoders as needed
            return payload_bytes # Return raw if unmapped
            
        except struct.error:
            return None
