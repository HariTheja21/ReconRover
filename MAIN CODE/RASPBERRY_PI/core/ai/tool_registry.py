from typing import Callable, Dict, Any, List

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        
    def register_tool(self, name: str, description: str, parameters: Dict[str, Any], callback: Callable):
        self.tools[name] = {
            "description": description,
            "parameters": parameters,
            "callback": callback
        }
        
    def get_tool(self, name: str) -> Dict[str, Any]:
        return self.tools.get(name)
        
    def list_tools(self) -> List[Dict[str, Any]]:
        result = []
        for name, meta in self.tools.items():
            result.append({
                "name": name,
                "description": meta["description"],
                "parameters": meta["parameters"]
            })
        return result
