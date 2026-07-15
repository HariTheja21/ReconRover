import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.agents.agent_runtime import AgentRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Multi-Agent Runtime...")
    bus = MockEventBus()
    runtime = AgentRuntime(bus)
    
    await runtime.initialize()
    
    print("\nListing Registered Agents...")
    agents = runtime.registry.get_all()
    for a in agents:
        print(f" - {a.agent_id} ({a.role})")
        
    print("\nWriting to Blackboard...")
    runtime.blackboard.write("mission_state", "exploring", "planner_1")
    state = runtime.blackboard.read("mission_state")
    print(f"Blackboard State: {state}")
    
    print("\nSending Inter-Agent Message...")
    await runtime.mailbox.send("vision_1", {"cmd": "analyze"})
    msg = await runtime.mailbox.receive("vision_1")
    print(f"Vision Agent received: {msg}")
    
    print("\nScheduling Task...")
    await runtime.scheduler.schedule_task("planner_1", {"id": "task_99", "action": "plan_route"})
    
    # Run scheduler briefly
    task = asyncio.create_task(runtime.scheduler.run_loop())
    await asyncio.sleep(0.5)
    task.cancel()
    
    print("\nChecking Consensus Manager...")
    agreement = runtime.consensus.reach_consensus("target", [{"agent_id": "vision_1", "val": "A"}, {"agent_id": "nav_1", "val": "B"}])
    print(f"Consensus Reached: {agreement}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
