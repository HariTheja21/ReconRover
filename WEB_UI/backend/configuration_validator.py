from typing import Dict, Any, Tuple

class ConfigurationValidator:
    @staticmethod
    def validate_configuration(config_data: Dict[str, Any]) -> Tuple[bool, str]:
        if not isinstance(config_data, dict):
            return False, "Configuration must be a JSON object."
            
        required_sections = ["motion_limits", "safety_thresholds", "communication"]
        for section in required_sections:
            if section not in config_data:
                return False, f"Missing required configuration section: {section}"
                
        # Basic bounds checking for motion limits
        motion = config_data.get("motion_limits", {})
        if "max_velocity" in motion and not (0 <= motion["max_velocity"] <= 10.0):
            return False, "max_velocity must be between 0 and 10.0"
            
        return True, "Valid"
