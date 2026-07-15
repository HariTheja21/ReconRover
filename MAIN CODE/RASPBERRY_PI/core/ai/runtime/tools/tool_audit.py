class ToolAudit:
    def __init__(self):
        self.logs = []
        
    def log_execution(self, tool_name: str, args: dict, result: dict):
        self.logs.append({"tool": tool_name, "args": args, "result": result})
