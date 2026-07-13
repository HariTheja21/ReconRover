// AUTO-GENERATED FILE. DO NOT MODIFY.
#ifndef ROVER_CONSTANTS_H
#define ROVER_CONSTANTS_H

// --- System Constants ---
constexpr const char* SYSTEM_FIRMWARE_VERSION = "2.0.0";
constexpr int SYSTEM_PROTOCOL_VERSION = 2;
constexpr int SYSTEM_MAX_MODULES = 32;
constexpr int SYSTEM_DEFAULT_TICK_RATE_HZ = 50;

// --- Communication Constants ---
constexpr int COMMUNICATION_BAUD_RATE = 115200;
constexpr int COMMUNICATION_MAX_PACKET_SIZE = 256;
constexpr int COMMUNICATION_SYNC_BYTE = 170;
constexpr int COMMUNICATION_TELEMETRY_PORT = 5000;
constexpr int COMMUNICATION_COMMAND_PORT = 5001;

// --- Safety Constants ---
constexpr float SAFETY_CRITICAL_BATTERY_V = 6.8;
constexpr float SAFETY_WARNING_BATTERY_V = 7.2;
constexpr int SAFETY_MAX_MOTOR_CURRENT_MA = 2000;
constexpr int SAFETY_EMERGENCY_STOP_DISTANCE_CM = 15;
constexpr int SAFETY_COMM_TIMEOUT_MS = 1000;

// --- Motion Constants ---
constexpr int MOTION_MIN_PWM = 0;
constexpr int MOTION_MAX_PWM = 255;
constexpr int MOTION_DEFAULT_SPEED = 150;
constexpr int MOTION_TURN_SPEED = 180;
constexpr int MOTION_ACCEL_STEP = 10;

// --- Servo Constants ---
constexpr int SERVO_PAN_MIN = 0;
constexpr int SERVO_PAN_MAX = 180;
constexpr int SERVO_PAN_CENTER = 90;
constexpr int SERVO_TILT_MIN = 30;
constexpr int SERVO_TILT_MAX = 150;
constexpr int SERVO_TILT_CENTER = 90;
constexpr int SERVO_DEFAULT_SPEED = 50;

// --- Sensors Constants ---
constexpr const char* SENSORS_MPU6050_ADDR = 0x68;
constexpr const char* SENSORS_VL53L0X_ADDR = 0x29;
constexpr const char* SENSORS_INA219_ADDR = 0x40;
constexpr const char* SENSORS_PCA9548A_ADDR = 0x70;

#endif // ROVER_CONSTANTS_H
