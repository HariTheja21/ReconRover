import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.llm.llm_runtime import LLMRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing LLM Runtime...")
    bus = MockEventBus()
    runtime = LLMRuntime(bus)
    
    await runtime.initialize()
    
    print("\nActivating OpenAI Provider...")
    runtime.auth.set_key("openai", "sk-mock-key")
    provider = await runtime.provider_manager.activate("openai", is_primary=True)
    print(f"OpenAI Activated: {provider is not None}")
    
    print("\nCreating Session...")
    session_id = "test-session-123"
    runtime.session.create_session(session_id)
    
    print("\nSubmitting Request via Scheduler...")
    await runtime.scheduler.submit_request("Hello, Recon Rover", session_id, "openai")
    
    # Run scheduler briefly to process the queue
    task = asyncio.create_task(runtime.scheduler.run_loop())
    await asyncio.sleep(0.5)
    task.cancel()
    
    print("\nChecking Context Memory...")
    context = runtime.session.get_context(session_id)
    print(f"Session Context: {context}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
