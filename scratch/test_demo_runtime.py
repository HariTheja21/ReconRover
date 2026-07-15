import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.demo.demo_runtime import DemoRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus -> {topic}] {payload}")

async def main():
    print("Initializing Full Autonomous AI Demonstration...")
    bus = MockEventBus()
    runtime = DemoRuntime(bus)
    
    await runtime.initialize()
    
    print("\n--- BEGIN MISSION DEMO ---")
    success = await runtime.manager.run_full_demo()
    
    print("\n--- END MISSION DEMO ---")
    print(f"Mission Success: {success}")
    
if __name__ == "__main__":
    asyncio.run(main())
