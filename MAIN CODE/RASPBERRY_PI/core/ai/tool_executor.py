import asyncio
import time
from typing import Dict, Any, Callable
from .tool_registry import ToolRegistry
from .ai_statistics import AIStatistics
from .ai_events import ToolExecutionEvent

class ToolExecutor:
    def __init__(self, registry: ToolRegistry, stats: AIStatistics, publish: Callable):
        self.registry = registry
        self.stats = stats
        self.publish = publish
        
    async def execute(self, tool_name: str, kwargs: Dict[str, Any]) -> Any:
        tool_meta = self.registry.get_tool(tool_name)
        if not tool_meta:
            raise ValueError(f"Tool {tool_name} not found")
            
        start_time = time.time()
        self.publish("ToolExecutionEvent", ToolExecutionEvent(tool_name, "START", 0, start_time))
        
        try:
            callback = tool_meta["callback"]
            if asyncio.iscoroutinefunction(callback):
                result = await callback(**kwargs)
            else:
                result = callback(**kwargs)
                
            latency = (time.time() - start_time) * 1000
            self.stats.total_tools_executed += 1
            self.publish("ToolExecutionEvent", ToolExecutionEvent(tool_name, "SUCCESS", latency, time.time()))
            return result
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.publish("ToolExecutionEvent", ToolExecutionEvent(tool_name, "FAILED", latency, time.time()))
            raise e
