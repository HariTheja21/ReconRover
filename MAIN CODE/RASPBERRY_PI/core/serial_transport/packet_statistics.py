"""
Packet Statistics Module
Recon Rover V2 - Phase 4.3
"""
import threading

class PacketStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.packets_sent = 0
        self.packets_received = 0
        self.framing_errors = 0
        self.reconnects = 0
        
    def increment_sent(self):
        with self._lock:
            self.packets_sent += 1
            
    def increment_received(self):
        with self._lock:
            self.packets_received += 1
            
    def increment_error(self):
        with self._lock:
            self.framing_errors += 1
            
    def increment_reconnect(self):
        with self._lock:
            self.reconnects += 1
