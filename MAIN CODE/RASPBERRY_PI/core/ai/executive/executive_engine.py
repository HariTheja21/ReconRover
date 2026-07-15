import asyncio

class ExecutiveEngine:
    def __init__(self, mission_exec, api):
        self.mission_exec = mission_exec
        self.api = api
        
    async def run_tick(self):
        await self.mission_exec.update_loop()
