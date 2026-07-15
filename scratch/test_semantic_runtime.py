import asyncio
import sys
import os

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.semantic.semantic_runtime import SemanticRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Semantic Mapping Runtime...")
    bus = MockEventBus()
    runtime = SemanticRuntime(bus)
    await runtime.initialize()
    
    print("\nIngesting Scene Update...")
    mock_scene = {
        "entities": [
            {"tracking_id": "1", "class": "bed", "x": 1.0, "y": 2.0, "z": 0.5},
            {"tracking_id": "2", "class": "chair", "x": 3.0, "y": 2.0, "z": 0.0}
        ]
    }
    await runtime.ingest_scene_update(mock_scene)
    
    print("\nCreating Landmark...")
    await runtime.request_landmark_creation("Charging Station", 0.0, 0.0, 0.0)
    
    # Wait for async scheduler to process
    await asyncio.sleep(0.1)
    
    print("\nExecuting Semantic Query for 'bed'...")
    results = runtime.execute_query("bed")
    print(f"Query Results: {results}")
    
    print("\nSemantic Statistics:")
    print(runtime.manager.stats.__dict__)
    
    runtime.shutdown()
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
