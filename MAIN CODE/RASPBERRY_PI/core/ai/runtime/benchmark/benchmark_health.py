class BenchmarkHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.active_profilers: int = 0

    def register_profiler(self):
        self.active_profilers += 1

    def unregister_profiler(self):
        self.active_profilers = max(0, self.active_profilers - 1)
