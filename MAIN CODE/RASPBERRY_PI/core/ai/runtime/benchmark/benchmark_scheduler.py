import asyncio

class BenchmarkScheduler:
    def __init__(self, manager):
        self.manager = manager
        
    async def run_loop(self):
        while True:
            self.manager.run_benchmark_cycle()
            await asyncio.sleep(300) # Profile every 5 minutes
