"""
utils/crc.py
Recon Rover V1 - Cognitive Layer

Calculates CCITT CRC-16 (polynomial 0x1021) matching the ESP32 implementation.
"""

def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

def format_hex_crc(crc: int) -> str:
    return f"{crc:04X}"
