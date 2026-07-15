import asyncio
import sys
import os
import numpy as np

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.perception.perception_runtime import PerceptionRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Perception AI Runtime...")
    bus = MockEventBus()
    runtime = PerceptionRuntime(bus)
    await runtime.initialize()
    
    print("\nSimulating Perception Cycle...")
    
    # Mock data from vision and navigation
    mock_detections = [
        {"tracking_id": "1", "class_name": "person", "confidence": 0.9, "bbox": [100, 100, 50, 150]},
        {"tracking_id": "2", "class_name": "table", "confidence": 0.85, "bbox": [120, 150, 100, 50]}
    ]
    mock_depth = np.ones((480, 640), dtype=np.float32) * 2.5 # 2.5 meters
    mock_pose = {"x": 10.0, "y": 5.0, "theta": 0.0}
    
    print("Ingesting Data...")
    await runtime.ingest_vision(mock_detections, mock_depth, mock_pose)
    
    # Let async scheduler process
    await asyncio.sleep(0.1)
    
    print("\nPerception Statistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nScene Graph Snapshot:")
    snapshot = runtime.manager.graph.get_snapshot()
    print(f"Entities: {snapshot['entities']}")
    print(f"Relationships: {snapshot['relationships']}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
