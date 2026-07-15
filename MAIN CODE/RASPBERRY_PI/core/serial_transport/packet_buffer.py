"""
Packet Buffer Module
Recon Rover V2 - Phase 4.3
"""
import threading

class PacketBuffer:
    """Thread-safe byte buffer for incoming UART stream."""
    def __init__(self, max_size=4096):
        self._lock = threading.RLock()
        self.buffer = bytearray()
        self.max_size = max_size
        
    def add(self, data: bytes):
        with self._lock:
            self.buffer.extend(data)
            if len(self.buffer) > self.max_size:
                # Discard oldest to prevent memory blowup on bad comms
                self.buffer = self.buffer[-self.max_size:]
                
    def read_all(self) -> bytearray:
        with self._lock:
            return self.buffer
            
    def consume(self, count: int):
        with self._lock:
            self.buffer = self.buffer[count:]
            
    def clear(self):
        with self._lock:
            self.buffer.clear()
