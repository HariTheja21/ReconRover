class LatencyMonitor:
    def __init__(self, publish):
        self.publish = publish
        
    def record_latency(self, subsystem: str, latency_ms: float):
        self.publish("LatencyUpdated", {"subsystem": subsystem, "latency_ms": latency_ms, "timestamp": 0.0})
