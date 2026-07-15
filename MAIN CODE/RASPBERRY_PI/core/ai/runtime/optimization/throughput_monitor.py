class ThroughputMonitor:
    def __init__(self, publish):
        self.publish = publish
        
    def record_throughput(self, subsystem: str, rps: float):
        self.publish("ThroughputUpdated", {"subsystem": subsystem, "requests_per_second": rps, "timestamp": 0.0})
