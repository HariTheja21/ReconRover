from typing import Dict, Any

class InputValidator:
    VALID_COMMANDS = {
        "DRIVE_FORWARD", "DRIVE_REVERSE", "TURN_LEFT", "TURN_RIGHT",
        "STOP", "EMERGENCY_STOP", "SPEED_CHANGE", "MODE_CHANGE",
        "MISSION_PAUSE", "MISSION_RESUME"
    }

    @staticmethod
    def validate(command: str, payload: Dict[str, Any]) -> bool:
        if command not in InputValidator.VALID_COMMANDS:
            return False
            
        if command == "SPEED_CHANGE":
            speed = payload.get("speed")
            if not isinstance(speed, (int, float)) or speed < 0 or speed > 100:
                return False
                
        if command in ["DRIVE_FORWARD", "DRIVE_REVERSE", "TURN_LEFT", "TURN_RIGHT"]:
            throttle = payload.get("throttle")
            if not isinstance(throttle, (int, float)) or throttle < 0 or throttle > 100:
                return False

        return True
