import asyncio
import sys
import os

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.ai_runtime import AIRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def test_tool(x: int, y: int):
    await asyncio.sleep(0.1)
    return x + y

async def main():
    print("Initializing AI Runtime...")
    bus = MockEventBus()
    runtime = AIRuntime(bus)
    await runtime.initialize()
    
    print("\nRegistering Mock Llama Model...")
    runtime.register_model("llama-3-8b", {
        "type": "llm",
        "requires_gpu": False,
        "required_memory_mb": 2048
    })
    
    print("\nLoading Model...")
    success = runtime.load_model("llama-3-8b")
    print(f"Load Success: {success}")
    
    print("\nRegistering Tool...")
    runtime.register_tool("add_numbers", "Adds two numbers", {"x": "int", "y": "int"}, test_tool)
    
    print("\nUpdating Context...")
    runtime.update_context("system", "battery", "85%")
    
    print("\nExecuting Task...")
    result = await runtime.execute_task("You are an AI assistant.", "What is the battery level?")
    print(f"Result: {result}")
    
    print("\nExecuting Tool directly via manager...")
    tool_res = await runtime.manager.tool_executor.execute("add_numbers", {"x": 5, "y": 10})
    print(f"Tool Result: {tool_res}")
    
    print("\nStatistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
