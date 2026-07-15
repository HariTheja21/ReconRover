import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.tools.tool_runtime import ToolRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Tool Runtime...")
    bus = MockEventBus()
    runtime = ToolRuntime(bus)
    
    await runtime.initialize()
    
    print("\nGetting Registered Tools Schema...")
    schemas = runtime.registry.get_all_schemas()
    for s in schemas:
        print(f" - {s['name']}: {s['description']}")
        
    print("\nDispatching Valid Tool...")
    res = await runtime.dispatcher.dispatch("navigation", {"direction": "forward"}, role="planner")
    print(f"Result: {res}")
    
    print("\nDispatching Tool with Invalid Role (Permissions check)...")
    res = await runtime.dispatcher.dispatch("system", {"command": "reboot"}, role="guest")
    print(f"Result: {res}")
    
    print("\nChecking Audit Log...")
    for log in runtime.audit.logs:
        print(log)

if __name__ == "__main__":
    asyncio.run(main())
