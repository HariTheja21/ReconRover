class ToolPermissions:
    def __init__(self):
        self.allowed_roles = ["admin", "planner", "executive"]
        
    def check_permission(self, tool_name: str, requester_role: str) -> bool:
        return requester_role in self.allowed_roles
