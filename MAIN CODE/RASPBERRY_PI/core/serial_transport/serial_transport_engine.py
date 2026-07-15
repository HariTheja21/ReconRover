"""
Serial Transport Engine Module
Recon Rover V2 - Phase 4.3
"""
from typing import List, Optional
from .serial_port import SerialPort
from .packet_sender import PacketSender
from .packet_receiver import PacketReceiver

class SerialTransportEngine:
    """Core logic for UART transport."""
    def __init__(self, stats, port: str = "/dev/serial0", baudrate: int = 115200):
        self.stats = stats
        self.serial = SerialPort(port, baudrate)
        self.sender = PacketSender()
        self.receiver = PacketReceiver(self.stats)
        
    def connect(self) -> bool:
        if self.serial.connect():
            self.stats.increment_reconnect()
            return True
        return False
        
    def disconnect(self):
        self.serial.disconnect()
        self.sender.clear()
        self.receiver.buffer.clear()
        
    def is_connected(self) -> bool:
        return self.serial.is_connected()
        
    def queue_outgoing(self, packet: bytes, force_front: bool = False):
        self.sender.queue_packet(packet, force_front)
        
    def process_tx(self) -> bool:
        """Sends one queued packet if connected. Returns True if sent."""
        if not self.is_connected():
            return False
            
        packet = self.sender.get_next()
        if packet:
            success = self.serial.write(packet)
            if success:
                self.stats.increment_sent()
            return success
        return False
        
    def process_rx(self) -> List[bytes]:
        """Reads from port and returns framed packets."""
        if not self.is_connected():
            return []
            
        data = self.serial.read_all()
        if data:
            packets = self.receiver.process_incoming(data)
            for p in packets:
                self.stats.increment_received()
            return packets
        return []
