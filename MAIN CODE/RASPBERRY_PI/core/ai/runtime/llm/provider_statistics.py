class ProviderStatistics:
    def __init__(self):
        self.stats = {}
        
    def log_request(self, provider: str, latency: float, success: bool):
        if provider not in self.stats:
            self.stats[provider] = {"requests": 0, "latency": 0.0, "errors": 0}
        self.stats[provider]["requests"] += 1
        self.stats[provider]["latency"] = (self.stats[provider]["latency"] + latency) / 2
        if not success:
            self.stats[provider]["errors"] += 1
