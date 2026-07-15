class SystemValidator:
    def validate_profile(self, profile: dict) -> bool:
        # A fully successful calibration requires all components to report status = ok
        required_keys = ["serial", "camera", "imu", "motor", "servo", "battery"]
        for key in required_keys:
            if key not in profile:
                return False
            if profile[key].get("status") != "ok":
                return False
        return True
