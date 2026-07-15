"""
Serial Statistics Module
Recon Rover V2 - Phase 2.4

Maintains thread-safe physical layer byte statistics.
"""

import threading

class SerialStatistics:
    """
    Data store for raw Serial counters.
    """
    
    def __init__(self):
        self._lock = threading.RLock()
        self.bytes_rx = 0
        self.bytes_tx = 0
        self.crc_errors = 0
        self.dropped_packets = 0
        self.valid_packets_rx = 0
        self.valid_packets_tx = 0
        
    def add_rx(self, num_bytes: int):
        with self._lock:
            self.bytes_rx += num_bytes
            
    def add_tx(self, num_bytes: int):
        with self._lock:
            self.bytes_tx += num_bytes
            
    def add_crc_error(self):
        with self._lock:
            self.crc_errors += 1
            
    def add_dropped(self):
        with self._lock:
            self.dropped_packets += 1
            
    def add_valid_rx(self):
        with self._lock:
            self.valid_packets_rx += 1
            
    def add_valid_tx(self):
        with self._lock:
            self.valid_packets_tx += 1
            
    def get_snapshot(self) -> dict:
        with self._lock:
            return {
                "bytes_rx": self.bytes_rx,
                "bytes_tx": self.bytes_tx,
                "crc_errors": self.crc_errors,
                "dropped_packets": self.dropped_packets,
                "valid_packets_rx": self.valid_packets_rx,
                "valid_packets_tx": self.valid_packets_tx
            }
