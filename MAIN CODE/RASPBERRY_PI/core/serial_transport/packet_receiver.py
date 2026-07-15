"""
Packet Receiver Module
Recon Rover V2 - Phase 4.3
"""
from typing import List
from .packet_buffer import PacketBuffer
from .packet_framer import PacketFramer

class PacketReceiver:
    """Processes incoming bytes and frames them into packets."""
    def __init__(self, stats):
        self.stats = stats
        self.buffer = PacketBuffer()
        self.framer = PacketFramer()
        
    def process_incoming(self, data: bytes) -> List[bytes]:
        """Returns a list of complete packets found in the stream."""
        if not data:
            return []
            
        self.buffer.add(data)
        packets = []
        
        while True:
            current_buffer = self.buffer.read_all()
            if not current_buffer:
                break
                
            packet, consume = self.framer.find_packet(current_buffer)
            
            if consume > 0:
                self.buffer.consume(consume)
                if packet is None:
                    # We consumed junk bytes
                    self.stats.increment_error()
            
            if packet:
                packets.append(packet)
            else:
                break
                
        return packets
