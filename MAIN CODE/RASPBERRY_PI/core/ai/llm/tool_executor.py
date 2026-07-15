import asyncio

class ToolExecutor:
    def __init__(self):
        self.available_tools = {}
        
    def register_tool(self, name: str, func):
        self.available_tools[name] = func
        
    async def execute(self, tool_name: str, args: dict) -> any:
        if tool_name in self.available_tools:
            return await self.available_tools[tool_name](**args)
        return f"Error: Tool {tool_name} not found."
