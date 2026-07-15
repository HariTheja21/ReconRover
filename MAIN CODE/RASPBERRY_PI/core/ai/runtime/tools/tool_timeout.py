import asyncio

class ToolTimeout:
    def __init__(self, default_timeout: float = 5.0):
        self.default_timeout = default_timeout
        
    async def execute_with_timeout(self, coro, timeout: float = None):
        t = timeout if timeout else self.default_timeout
        try:
            return await asyncio.wait_for(coro, timeout=t)
        except asyncio.TimeoutError:
            return {"status": "error", "message": "Execution timed out"}
