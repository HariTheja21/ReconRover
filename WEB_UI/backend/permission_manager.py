from typing import List
from .role_manager import RoleManager
from .collaboration_statistics import CollaborationStatistics

class PermissionManager:
    def __init__(self, role_manager: RoleManager, stats: CollaborationStatistics):
        self.role_manager = role_manager
        self.stats = stats

    def has_permission(self, role: str, required_permission: str) -> bool:
        perms = self.role_manager.get_role_permissions(role)
        if required_permission in perms:
            return True
        self.stats.total_permission_denials += 1
        return False
