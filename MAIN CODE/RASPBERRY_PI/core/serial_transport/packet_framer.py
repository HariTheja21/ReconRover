"""
Packet Framer Module
Recon Rover V2 - Phase 4.3
"""

class PacketFramer:
    """Identifies and extracts full packets from a byte stream."""
    def __init__(self):
        self.HEADER = b'\xAA\x55'
        self.PACKET_LENGTH = 9 # Shared Protocol Size
        
    def find_packet(self, buffer: bytearray) -> tuple:
        """
        Returns (packet_bytes, bytes_to_consume)
        If no packet found, returns (None, bytes_to_consume)
        """
        idx = buffer.find(self.HEADER)
        if idx == -1:
            # Header not found. Consume everything except the last byte 
            # (which might be the start of a header '0xAA').
            consume = max(0, len(buffer) - 1)
            return None, consume
            
        # We found a header. Do we have the full packet?
        if len(buffer) - idx >= self.PACKET_LENGTH:
            # Extract packet
            packet = bytes(buffer[idx:idx+self.PACKET_LENGTH])
            return packet, idx + self.PACKET_LENGTH
            
        # Found header but packet is incomplete. Wait for more data.
        return None, idx
