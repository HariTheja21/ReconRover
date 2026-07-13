"""
al_health.py
Recon Rover V1 - Audio-Language Cognitive Integration

Tracks the health of the AL cognitive layer.
"""

class ALHealth:
    def __init__(self):
        self.status = "OK"
        self.errors = 0
        
    def record_error(self):
        self.errors += 1
        if self.errors > 5:
            self.status = "DEGRADED"
            
    def record_success(self):
        self.errors = 0
        self.status = "OK"
