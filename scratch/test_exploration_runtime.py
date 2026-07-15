import asyncio
import sys
import os
import numpy as np

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.exploration.exploration_runtime import ExplorationRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Autonomous Exploration Runtime...")
    bus = MockEventBus()
    runtime = ExplorationRuntime(bus)
    await runtime.initialize()
    
    print("\nStarting Exploration...")
    runtime.start_exploration()
    
    print("\nUpdating Pose...")
    runtime.update_robot_pose(5.0, 5.0)
    
    print("\nIngesting Map Grid...")
    # Mock a 100x100 grid
    mock_grid = np.zeros((100, 100))
    await runtime.ingest_occupancy_grid(mock_grid, 0.05, (0, 0))
    
    # Wait for scheduler to process
    await asyncio.sleep(0.1)
    
    print("\nExploration Statistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nExploration State:")
    print(f"Current State: {runtime.manager.state.get_state()}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
