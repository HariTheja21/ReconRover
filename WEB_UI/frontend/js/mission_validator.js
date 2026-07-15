class MissionValidator {
    static validate(name, waypoints) {
        if (!name || name.trim() === "") {
            return { valid: false, message: "Mission name is required." };
        }
        if (waypoints.length === 0) {
            return { valid: false, message: "Mission must have at least one waypoint." };
        }
        return { valid: true, message: "" };
    }
}
