from typing import Dict, List, Any
from .security_statistics import SecurityStatistics
from .security_events import AuthorizationEvent
import time

class AuthorizationManager:
    def __init__(self, stats: SecurityStatistics):
        self.stats = stats
        # RBAC definitions (copied from Phase 6.7 RoleManager for security decoupling)
        self.roles = {
            "Administrator": ["DRIVE", "MISSION", "CONFIG", "OTA", "DIAG", "ESTOP"],
            "Mission Commander": ["MISSION", "CAMERA", "DIAG", "ESTOP"],
            "Pilot": ["DRIVE", "CAMERA", "ESTOP"],
            "Observer": ["CAMERA", "DIAG"],
            "Diagnostics": ["DIAG", "CONFIG"],
            "Maintenance": ["CONFIG", "OTA", "DIAG", "ESTOP"]
        }

    def check_permission(self, role: str, required_permission: str) -> bool:
        if role not in self.roles:
            self.stats.total_authorizations_denied += 1
            return False
            
        if required_permission in self.roles[role]:
            self.stats.total_authorizations_granted += 1
            return True
            
        self.stats.total_authorizations_denied += 1
        return False
