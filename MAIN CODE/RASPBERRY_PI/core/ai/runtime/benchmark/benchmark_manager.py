class BenchmarkManager:
    def __init__(self, profilers: list, store, report_generator):
        self.profilers = profilers
        self.store = store
        self.report_generator = report_generator
        
    def run_benchmark_cycle(self):
        results = {}
        for profiler in self.profilers:
            name = profiler.__class__.__name__
            val = profiler.measure()
            self.store.store_metric(name, val)
            results[name] = val
        return results
