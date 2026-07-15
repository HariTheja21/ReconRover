import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class AgentScheduler:
    def __init__(self, engine: Any, registry: Any):
        self.engine = engine
        self.registry = registry
        
    async def run_agent_loops(self):
        logger.info("Starting Agent Loops")
        tasks = []
        for agent in self.registry.get_all_agents():
            tasks.append(asyncio.create_task(agent.run()))
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
    async def run_coordination_loop(self):
        while True:
            try:
                await self.engine.monitor_conflicts()
                await asyncio.sleep(1.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Coordination Loop: {e}")
                await asyncio.sleep(1.0)
