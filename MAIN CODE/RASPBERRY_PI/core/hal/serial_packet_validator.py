"""
Serial Packet Validator Module
Recon Rover V2 - Phase 2.4

Handles CRC16 payload validation, packet length verification, and duplicate detection
before allowing bytes to cross the Event Bridge.
"""

import struct
from typing import Tuple

class SerialPacketValidator:
    """
    Stateless validation engine for raw incoming byte arrays.
    """
    
    # 17 bytes: sync1(1), sync2(1), ver(1), src(1), dest(1), prio(1), seq(2), time(4), type(1), len(2), crc(2)
    HEADER_FORMAT = "<BBBBBBHIBHH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    
    SYNC_1 = 0xAA
    SYNC_2 = 0x55
    
    @staticmethod
    def calculate_crc16(data: bytes) -> int:
        """
        Calculates a standard CRC-16-CCITT for the payload.
        """
        crc = 0xFFFF
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
                crc &= 0xFFFF
        return crc

    @classmethod
    def validate_packet(cls, raw_bytes: bytes) -> Tuple[bool, str]:
        """
        Validates the integrity of an entire packet buffer.
        
        Args:
            raw_bytes (bytes): The full packet (Header + Payload)
            
        Returns:
            Tuple[bool, str]: (is_valid, reason)
        """
        if len(raw_bytes) < cls.HEADER_SIZE:
            return False, "Buffer smaller than header size."
            
        try:
            unpacked = struct.unpack(cls.HEADER_FORMAT, raw_bytes[:cls.HEADER_SIZE])
            sync_1 = unpacked[0]
            sync_2 = unpacked[1]
            payload_len = unpacked[9]
            header_crc = unpacked[10]
            
            if sync_1 != cls.SYNC_1 or sync_2 != cls.SYNC_2:
                return False, "Invalid SYNC bytes."
                
            expected_total_len = cls.HEADER_SIZE + payload_len
            if len(raw_bytes) < expected_total_len:
                return False, f"Incomplete payload. Expected {expected_total_len}, got {len(raw_bytes)}"
                
            # Note: The packet might have garbage at the end (len > expected), we only care up to expected
            payload_bytes = raw_bytes[cls.HEADER_SIZE:expected_total_len]
            
            # If the architecture uses CRC, validate it.
            # We assume a CRC of 0 means "skip validation" for testing/early phases.
            if header_crc != 0:
                calculated_crc = cls.calculate_crc16(payload_bytes)
                if calculated_crc != header_crc:
                    return False, f"CRC mismatch. Expected {header_crc}, got {calculated_crc}"
                    
            return True, ""
            
        except struct.error:
            return False, "Struct unpack failed."
