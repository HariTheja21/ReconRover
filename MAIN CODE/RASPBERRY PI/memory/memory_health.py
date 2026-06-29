"""
memory_health.py
Recon Rover V1 - Persistent Memory

Tracks database write errors and index staleness.
"""

class MemoryHealth:
    def __init__(self):
        self.status = "OK"
        self.consecutive_errors = 0

    def record_error(self):
        self.consecutive_errors += 1
        if self.consecutive_errors > 3:
            self.status = "DEGRADED"
        if self.consecutive_errors > 10:
            self.status = "CRITICAL (DB FAILED)"

    def record_success(self):
        self.consecutive_errors = 0
        self.status = "OK"
