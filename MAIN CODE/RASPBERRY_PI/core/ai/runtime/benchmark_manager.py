class BenchmarkManager:
    def __init__(self, publish):
        self.publish = publish
        
    def run_benchmark(self, model_name: str):
        # Stub benchmark
        metrics = {"latency_ms": 150, "throughput_tps": 20}
        self.publish("BenchmarkCompleted", {
            "model_name": model_name,
            "metrics": metrics,
            "timestamp": 0.0
        })
        return metrics
