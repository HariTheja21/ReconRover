"""
serial_health.py
Recon Rover V1 - Serial Communication Manager

Monitors the overall health state of the serial subsystem.
"""

class SerialHealth:
    def __init__(self):
        self.is_connected = False
        self.error_state = False
        self.last_heartbeat_ms = 0

    def update_heartbeat(self, timestamp_ms: int):
        self.last_heartbeat_ms = timestamp_ms
        self.error_state = False

    def get_status_string(self) -> str:
        if not self.is_connected:
            return "DISCONNECTED"
        if self.error_state:
            return "ERROR_STATE"
        return "OK"
