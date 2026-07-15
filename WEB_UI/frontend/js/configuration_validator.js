class ConfigurationValidator {
    static validate(config) {
        if(config.motion.max_velocity < 0 || config.motion.max_velocity > 5.0) {
            return { valid: false, message: "Max velocity must be between 0 and 5.0 m/s" };
        }
        if(config.safety.battery_critical < 9.0 || config.safety.battery_critical > 12.0) {
            return { valid: false, message: "Critical battery voltage out of safe bounds (9-12V)" };
        }
        return { valid: true, message: "Valid" };
    }
}
