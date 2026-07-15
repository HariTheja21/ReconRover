from typing import Dict, List, Any

class RoleManager:
    def __init__(self):
        self.roles = {
            "Administrator": ["DRIVE", "MISSION", "CONFIG", "OTA", "DIAG", "ESTOP"],
            "Mission Commander": ["MISSION", "CAMERA", "DIAG", "ESTOP"],
            "Pilot": ["DRIVE", "CAMERA", "ESTOP"],
            "Observer": ["CAMERA", "DIAG"],
            "Diagnostics": ["DIAG", "CONFIG"],
            "Maintenance": ["CONFIG", "OTA", "DIAG", "ESTOP"]
        }
        
    def get_role_permissions(self, role: str) -> List[str]:
        return self.roles.get(role, [])

    def is_valid_role(self, role: str) -> bool:
        return role in self.roles
