from typing import Dict, Any

class MissionValidator:
    VALID_TYPES = {"Waypoint Mission", "Patrol Mission", "Inspection Mission", "Exploration Mission"}

    @staticmethod
    def validate_mission(mission_data: Dict[str, Any]) -> tuple[bool, str]:
        if "name" not in mission_data or not mission_data["name"]:
            return False, "Mission name is required."
            
        m_type = mission_data.get("type")
        if m_type not in MissionValidator.VALID_TYPES:
            return False, f"Invalid mission type: {m_type}"
            
        waypoints = mission_data.get("waypoints", [])
        if not isinstance(waypoints, list):
            return False, "Waypoints must be a list."
            
        if len(waypoints) == 0:
            return False, "Mission must have at least one waypoint."
            
        for idx, wp in enumerate(waypoints):
            if "lat" not in wp or "lng" not in wp:
                return False, f"Waypoint {idx} is missing lat/lng coordinates."
            if not isinstance(wp["lat"], (int, float)) or not isinstance(wp["lng"], (int, float)):
                return False, f"Waypoint {idx} coordinates must be numbers."
                
        return True, "Valid"
