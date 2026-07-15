import asyncio
import sys
import os

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.runtime_manager import RuntimeManager

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing AI Environment Runtime...")
    bus = MockEventBus()
    runtime = RuntimeManager(bus)
    
    # Register mock providers
    runtime.prov_reg.register("onnx", {"deps": ["onnxruntime"]})
    runtime.prov_reg.register("ollama", {"deps": ["requests"]})
    
    success = await runtime.initialize()
    print(f"Environment Validated: {success}")
    
    print("\nLoading Providers...")
    res = await runtime.loader.load_runtime(["onnx", "ollama"])
    print(res)
    
    print("\nDownloading Model...")
    await runtime.repo.get_model("llama3", "latest")
    print(f"Cache state: {runtime.cache.cached_models}")
    
    print("\nRunning Benchmark...")
    metrics = runtime.bench_mgr.run_benchmark("llama3")
    print(metrics)
    
    await asyncio.sleep(0.5)
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
