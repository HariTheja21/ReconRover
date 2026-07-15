class ToolRegistry:
    def __init__(self):
        self._tools = {}
        
    def register(self, tool):
        self._tools[tool.name] = tool
        
    def get_tool(self, name: str):
        return self._tools.get(name)
        
    def get_all_schemas(self) -> list:
        return [{"name": t.name, "description": t.description, "schema": t.get_schema()} for t in self._tools.values()]
