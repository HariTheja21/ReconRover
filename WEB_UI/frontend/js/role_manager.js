class RoleManager {
    constructor() {
        this.roles = {
            "Administrator": ["DRIVE", "MISSION", "CONFIG", "OTA", "DIAG", "ESTOP"],
            "Mission Commander": ["MISSION", "CAMERA", "DIAG", "ESTOP"],
            "Pilot": ["DRIVE", "CAMERA", "ESTOP"],
            "Observer": ["CAMERA", "DIAG"],
            "Diagnostics": ["DIAG", "CONFIG"],
            "Maintenance": ["CONFIG", "OTA", "DIAG", "ESTOP"]
        };
    }
    
    hasPermission(role, permission) {
        if (!this.roles[role]) return false;
        return this.roles[role].includes(permission);
    }
}
