"""
Packet Builder Module
Recon Rover V2 - Phase 4.2
"""
import struct
import threading

class PacketBuilder:
    """
    Constructs binary payloads matching the SHARED protocol definitions.
    Format: [HEADER] [CMD_TYPE] [SEQ_NUM] [PAYLOAD_L] [PAYLOAD_R] [CRC8]
    HEADER: 0xAA 0x55 (2 bytes)
    CMD_TYPE: 0x01 (Velocity) (1 byte)
    SEQ_NUM: (1 byte, 0-255)
    PAYLOAD_L: (2 bytes, int16)
    PAYLOAD_R: (2 bytes, int16)
    CRC8: (1 byte)
    Total: 9 bytes
    """
    def __init__(self):
        self._lock = threading.RLock()
        self.HEADER = b'\xAA\x55'
        self.CMD_VELOCITY = 0x01
        
    def compute_crc8(self, data: bytes) -> int:
        """Simple XOR CRC for testing."""
        crc = 0
        for b in data:
            crc ^= b
        return crc
        
    def build_velocity_packet(self, seq_num: int, enc_left: int, enc_right: int) -> bytes:
        with self._lock:
            # Pack payload: [CMD_TYPE, SEQ_NUM, LEFT(short), RIGHT(short)]
            # >B B h h means big-endian: unsigned char, unsigned char, short, short
            payload = struct.pack('>BBhh', self.CMD_VELOCITY, seq_num, enc_left, enc_right)
            
            crc = self.compute_crc8(payload)
            
            # Full packet: HEADER + payload + crc
            packet = self.HEADER + payload + struct.pack('>B', crc)
            return packet
