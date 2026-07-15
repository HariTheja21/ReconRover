import asyncio
import sys
import os

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.executive.executive_runtime import ExecutiveRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Executive Runtime...")
    bus = MockEventBus()
    runtime = ExecutiveRuntime(bus)
    await runtime.initialize()
    
    print("\nStarting Mission...")
    mission_id = await runtime.execute_mission({"type": "PATROL"})
    print(f"Mission ID: {mission_id}")
    
    # Wait for async scheduler and task loops to process
    await asyncio.sleep(0.5)
    
    print(f"\nMission State: {runtime.manager.sm.get_state()}")
    
    print("\nExecutive Statistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nAborting Mission...")
    await runtime.abort_mission()
    
    await asyncio.sleep(0.1)
    print(f"Mission State: {runtime.manager.sm.get_state()}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
