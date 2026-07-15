import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.benchmark.benchmark_runtime import BenchmarkRuntime

class MockEventBus:
    def publish(self, topic, payload):
        pass # print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Benchmark Runtime...")
    bus = MockEventBus()
    runtime = BenchmarkRuntime(bus)
    
    await runtime.initialize()
    
    print(f"Loaded {len(runtime.profilers)} Profilers.")
    
    print("\nRunning Benchmark Cycle...")
    res = runtime.manager.run_benchmark_cycle()
    print("Cycle complete. Profiles captured:")
    for k, v in res.items():
        print(f" - {k}: {v}")
        
    print("\nGenerating Report...")
    report = runtime.report_generator.generate_summary()
    print(f"Report: {report}")
    
    print("\nExporting JSON Data...")
    json_data = runtime.exporter.export_json()
    print(f"Export String Length: {len(json_data)} chars")
    
if __name__ == "__main__":
    asyncio.run(main())
