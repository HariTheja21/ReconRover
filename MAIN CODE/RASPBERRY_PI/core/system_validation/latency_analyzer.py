class LatencyAnalyzer:
    def __init__(self):
        self.latencies = []

    def record_latency(self, latency_ms: int):
        self.latencies.append(latency_ms)

    def get_average_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return sum(self.latencies) / len(self.latencies)
        
    def get_max_latency(self) -> int:
        if not self.latencies:
            return 0
        return max(self.latencies)
        
    def validate_latency(self, max_allowed_ms: int) -> bool:
        return self.get_max_latency() <= max_allowed_ms
