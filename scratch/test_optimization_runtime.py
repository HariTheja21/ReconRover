import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.optimization.optimization_runtime import OptimizationRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Optimization Runtime...")
    bus = MockEventBus()
    runtime = OptimizationRuntime(bus)
    
    await runtime.initialize()
    
    print("\nRunning Memory & Cache Optimization...")
    res = runtime.manager.run_optimization_cycle()
    print(f"Optimization Cycle Result: {res}")
    
    print("\nTesting Resource Allocation (Priority 10)...")
    alloc = runtime.resource_allocator.allocate_resources({"id": "task_1", "priority": 10})
    print(f"Allocated: {alloc}")
    
    print("\nTesting Thermal Manager (High Temp)...")
    status = runtime.thermal_manager.check_temperature(90.0)
    print(f"Thermal Status: {status}")
    print(f"System Healthy? {runtime.health.is_healthy}")
    
    print("\nTesting Thermal Manager (Cooldown)...")
    status = runtime.thermal_manager.check_temperature(70.0)
    print(f"Thermal Status: {status}")
    print(f"System Healthy? {runtime.health.is_healthy}")
    
    print("\nTesting Priority Scheduler...")
    runtime.priority_scheduler.push_task(5, {"id": "low_pri_task"})
    runtime.priority_scheduler.push_task(1, {"id": "high_pri_task"})
    
    first = runtime.priority_scheduler.pop_task()
    second = runtime.priority_scheduler.pop_task()
    
    print(f"Popped first: {first}")
    print(f"Popped second: {second}")

if __name__ == "__main__":
    asyncio.run(main())
