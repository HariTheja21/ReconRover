"""
hardware_statistics.py
Recon Rover V1 - Hardware Interface

Monitors throughput.
"""

class HardwareStatistics:
    def __init__(self):
        self.bytes_tx = 0
        self.bytes_rx = 0
        
    def record_tx(self, count: int):
        self.bytes_tx += count
        
    def record_rx(self, count: int):
        self.bytes_rx += count
