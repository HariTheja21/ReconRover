class ProviderHealth:
    def __init__(self, publish):
        self.publish = publish
        self.status = {}
        
    def update(self, provider: str, is_healthy: bool, latency: float):
        self.status[provider] = is_healthy
        self.publish("ProviderHealthUpdated", {
            "provider": provider,
            "is_healthy": is_healthy,
            "latency_ms": latency,
            "timestamp": 0.0
        })
