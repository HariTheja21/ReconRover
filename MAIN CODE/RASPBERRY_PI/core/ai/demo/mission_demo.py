import asyncio

class MissionDemo:
    def __init__(self, coordinator, logger):
        self.coordinator = coordinator
        self.logger = logger
        
    async def execute_scenario(self, scenario: dict) -> bool:
        self.logger.log(f"Starting Mission Scenario: {scenario.get('id')}")
        for step in scenario.get("steps", []):
            res = self.coordinator.coordinate(step)
            self.logger.log(res)
            await asyncio.sleep(0.1) # Simulate execution time
        return True
