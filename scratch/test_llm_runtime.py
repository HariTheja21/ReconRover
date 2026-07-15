import asyncio
import sys
import os

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.llm.llm_runtime import LLMRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing LLM Runtime...")
    bus = MockEventBus()
    runtime = LLMRuntime(bus)
    await runtime.initialize()
    
    print("\nSubmitting Prompt: 'Analyze the living room scene'")
    await runtime.submit_prompt("Analyze the living room scene")
    
    # Wait for async scheduler and task loops to process
    await asyncio.sleep(0.5)
    
    print("\nLLM Statistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nConversation History:")
    for msg in runtime.manager.cm.get_history():
        print(f"[{msg['role'].upper()}]: {msg['content']}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
