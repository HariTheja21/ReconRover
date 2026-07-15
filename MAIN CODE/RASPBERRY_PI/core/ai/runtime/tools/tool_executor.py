class ToolExecutor:
    def __init__(self, validator, permissions, timeout, retry):
        self.validator = validator
        self.permissions = permissions
        self.timeout = timeout
        self.retry = retry
        
    async def execute(self, tool, args: dict, role: str) -> dict:
        if not self.permissions.check_permission(tool.name, role):
            return {"status": "error", "message": "Permission denied"}
            
        if not self.validator.validate_schema(args, tool.get_schema()):
            return {"status": "error", "message": "Invalid arguments schema"}
            
        return await self.retry.execute_with_retry(
            lambda: self.timeout.execute_with_timeout(tool.execute(**args))
        )
