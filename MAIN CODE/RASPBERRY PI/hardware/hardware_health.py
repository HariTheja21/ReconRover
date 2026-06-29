"""
hardware_health.py
Recon Rover V1 - Hardware Interface

Monitors the connection state of the hardware layer.
"""

class HardwareHealth:
    def __init__(self):
        self.status = "DISCONNECTED"
        self.packet_drops = 0
        
    def set_connected(self):
        self.status = "OK"
        
    def set_disconnected(self):
        self.status = "DISCONNECTED"
        
    def record_drop(self):
        self.packet_drops += 1
