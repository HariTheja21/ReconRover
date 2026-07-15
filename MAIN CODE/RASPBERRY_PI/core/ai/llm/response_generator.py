class ResponseGenerator:
    def __init__(self, engine):
        self.engine = engine
        
    async def generate(self, user_input: str, history: list) -> str:
        return await self.engine.reason(user_input, history)
