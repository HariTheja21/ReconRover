class ExecutiveAPI:
    def __init__(self, engine):
        self.engine = engine
        
    async def start_mission(self, params: dict):
        return await self.engine.start_mission(params)
        
    async def abort_mission(self):
        return await self.engine.abort_mission()
