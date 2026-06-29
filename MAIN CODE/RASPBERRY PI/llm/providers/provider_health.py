"""
provider_health.py
Recon Rover V1 - Local LLM Framework

Tracks health specifically for the underlying provider endpoint.
"""

class ProviderHealth:
    def __init__(self):
        self.is_online = False
        self.model_loaded = False
        self.average_latency = 0.0
        self.failures = 0
        self.timeouts = 0
        self.retries = 0

    def record_success(self, latency: float):
        self.is_online = True
        self.model_loaded = True
        # Rolling average of last 10 requests approx
        self.average_latency = (self.average_latency * 0.9) + (latency * 0.1)

    def record_failure(self, is_timeout: bool = False):
        self.failures += 1
        if is_timeout:
            self.timeouts += 1
        # If we get failures, we assume offline until proven otherwise
        self.is_online = False

    def record_retry(self):
        self.retries += 1
