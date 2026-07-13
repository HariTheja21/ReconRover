"""
vl_health.py
Recon Rover V1 - Vision-Language Cognitive Integration

Tracks the health of the VL cognitive layer.
"""

class VLHealth:
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
