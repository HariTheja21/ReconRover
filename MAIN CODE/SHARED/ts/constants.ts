// AUTO-GENERATED FILE. DO NOT MODIFY.

export const SystemConstants = {
    FIRMWARE_VERSION: "2.0.0",
    PROTOCOL_VERSION: 2,
    MAX_MODULES: 32,
    DEFAULT_TICK_RATE_HZ: 50,
    ROBOT_NAME: "Recon Rover V2",
    HARDWARE_REVISION: "RevB"
};

export const CommunicationConstants = {
    BAUD_RATE: 115200,
    MAX_PACKET_SIZE: 256,
    SYNC_BYTE_1: 0xAA,
    SYNC_BYTE_2: 0x55,
    TELEMETRY_PORT: 5000,
    COMMAND_PORT: 5001
};

export const SafetyConstants = {
    CRITICAL_BATTERY_V: 6.8,
    WARNING_BATTERY_V: 7.2,
    MAX_MOTOR_CURRENT_MA: 2000,
    EMERGENCY_STOP_DISTANCE_CM: 15.0,
    COMM_TIMEOUT_MS: 1000
};

export const MotionConstants = {
    MIN_PWM: 0,
    MAX_PWM: 255,
    DEFAULT_SPEED: 150,
    TURN_SPEED: 180,
    ACCEL_STEP: 10
};

export const ServoConstants = {
    PAN_MIN: 0,
    PAN_MAX: 180,
    PAN_CENTER: 90,
    TILT_MIN: 30,
    TILT_MAX: 150,
    TILT_CENTER: 90,
    DEFAULT_SPEED: 50
};

export const SensorsConstants = {
    MPU6050_ADDR: 0x68,
    VL53L0X_ADDR: 0x29,
    INA219_ADDR: 0x40,
    PCA9548A_ADDR: 0x70
};

export const DeveloperConstants = {
    DEBUG_MODE_ENABLED: true,
    VERBOSE_SERIAL_LOGGING: false,
    HEARTBEAT_INTERVAL_MS: 1000
};
