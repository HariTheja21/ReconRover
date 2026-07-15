import asyncio
import sys
import os

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.task_planner.task_planner_runtime import TaskPlannerRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Task Planner Runtime...")
    bus = MockEventBus()
    runtime = TaskPlannerRuntime(bus)
    await runtime.initialize()
    
    print("\nIngesting Mission: 'Explore living room'")
    await runtime.ingest_mission("Explore living room", {"priority": "HIGH"})
    
    # Wait for async scheduler and task loop to process
    await asyncio.sleep(0.5)
    
    print("\nPlanner Statistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
