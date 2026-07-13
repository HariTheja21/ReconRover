"""
autonomy_health.py
Recon Rover V1 - Autonomous Intelligence

Tracks the health of the autonomy layer.
"""

class AutonomyHealth:
    def __init__(self):
        self.status = "OK"
        self.consecutive_failures = 0

    def record_failure(self):
        self.consecutive_failures += 1
        if self.consecutive_failures > 3:
            self.status = "DEGRADED"
        if self.consecutive_failures > 10:
            self.status = "CRITICAL"

    def record_success(self):
        self.consecutive_failures = 0
        self.status = "OK"
