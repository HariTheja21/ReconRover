import uuid

class ToolDispatcher:
    def __init__(self, registry, executor, audit, publish):
        self.registry = registry
        self.executor = executor
        self.audit = audit
        self.publish = publish
        
    async def dispatch(self, tool_name: str, args: dict, role: str = "planner") -> dict:
        exec_id = str(uuid.uuid4())
        self.publish("ToolExecutionStarted", {"tool_name": tool_name, "execution_id": exec_id, "timestamp": 0.0})
        
        tool = self.registry.get_tool(tool_name)
        if not tool:
            err = {"status": "error", "message": "Tool not found"}
            self.publish("ToolExecutionFailed", {"tool_name": tool_name, "execution_id": exec_id, "error_message": "Tool not found", "timestamp": 0.0})
            return err
            
        result = await self.executor.execute(tool, args, role)
        
        self.audit.log_execution(tool_name, args, result)
        
        if result.get("status") == "error":
            self.publish("ToolExecutionFailed", {"tool_name": tool_name, "execution_id": exec_id, "error_message": result.get("message"), "timestamp": 0.0})
        else:
            self.publish("ToolExecutionCompleted", {"tool_name": tool_name, "execution_id": exec_id, "latency_ms": 10.0, "timestamp": 0.0})
            self.publish("ToolResultGenerated", {"tool_name": tool_name, "execution_id": exec_id, "result": result, "timestamp": 0.0})
            
        return result
