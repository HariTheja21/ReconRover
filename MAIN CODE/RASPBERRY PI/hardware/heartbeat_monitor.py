"""
heartbeat_monitor.py
Recon Rover V1 - Hardware Interface

Transmits heartbeat PINGs and triggers safety protocols if ACKs are missed.
"""

import time
from event_bus import EventBus, HeartbeatTimeout

class HeartbeatMonitor:
    def __init__(self, event_bus: EventBus, timeout_sec: float = 2.0):
        self.event_bus = event_bus
        self.timeout_sec = timeout_sec
        self.last_ack_time = time.time()
        self.is_healthy = True
        
    def record_ack(self):
        self.last_ack_time = time.time()
        self.is_healthy = True
        
    def check_health(self) -> bool:
        """Returns True if healthy. Triggers EventBus timeout if dead."""
        if not self.is_healthy:
            return False
            
        time_since_ack = time.time() - self.last_ack_time
        if time_since_ack > self.timeout_sec:
            self.is_healthy = False
            self.event_bus.publish(HeartbeatTimeout(
                last_seen=self.last_ack_time,
                time_since=time_since_ack
            ))
            return False
            
        return True
