// AUTO-GENERATED FILE. DO NOT MODIFY.
#ifndef ROVER_ENUMS_H
#define ROVER_ENUMS_H

#include <stdint.h>

enum class OperatingMode : uint8_t {
    STANDBY = 0,
    REMOTE = 1,
    SMART_CONTROL = 2,
    LEGEND_AI = 3,
    EMERGENCY = 99,
};

enum class MissionMode : uint8_t {
    IDLE = 0,
    OBSTACLE_AVOIDANCE = 1,
    EXPLORATION = 2,
    PERSON_FOLLOWING = 3,
    OBJECT_FOLLOWING = 4,
    MOTION_DETECTION = 5,
    SCENE_EXPLANATION = 6,
    HOME_ASSISTANT = 7,
    DIAGNOSTICS = 8,
    CALIBRATION = 9,
};

enum class CommandType : uint8_t {
    MOTION = 10,
    SERVO = 11,
    LED = 12,
    OLED = 13,
    CAMERA = 14,
    AUDIO = 15,
    SYSTEM = 16,
    MISSION = 17,
    CONFIG = 18,
};

enum class TelemetryType : uint8_t {
    HEARTBEAT = 20,
    SYSTEM_HEALTH = 21,
    BATTERY = 22,
    IMU = 23,
    DISTANCE = 24,
    ENVIRONMENT = 25,
    MOTOR_STATUS = 26,
    SERVO_STATUS = 27,
    LOG_MESSAGE = 28,
};

enum class EventType : uint8_t {
    SYSTEM_STARTUP = 100,
    SYSTEM_SHUTDOWN = 101,
    MODE_CHANGED = 102,
    MISSION_CHANGED = 103,
    CONFIG_CHANGED = 104,
    HARDWARE_FAULT = 105,
    SENSOR_READING = 106,
    AI_INFERENCE = 107,
};

enum class ConnectionState : uint8_t {
    DISCONNECTED = 0,
    CONNECTING = 1,
    CONNECTED = 2,
    ERROR = 3,
};

enum class BatteryState : uint8_t {
    FULL = 0,
    NORMAL = 1,
    WARNING = 2,
    CRITICAL = 3,
    CHARGING = 4,
};

enum class MotorState : uint8_t {
    STOPPED = 0,
    MOVING_FORWARD = 1,
    MOVING_REVERSE = 2,
    TURNING = 3,
    FAULT = 4,
};

enum class ServoState : uint8_t {
    IDLE = 0,
    MOVING = 1,
    STALLED = 2,
    ERROR = 3,
};

enum class CameraState : uint8_t {
    OFF = 0,
    STREAMING = 1,
    RECORDING = 2,
    ERROR = 3,
};

enum class LEDState : uint8_t {
    OFF = 0,
    SOLID = 1,
    BLINKING = 2,
    PULSING = 3,
    RAINBOW = 4,
};

enum class VoiceState : uint8_t {
    LISTENING = 0,
    PROCESSING = 1,
    SPEAKING = 2,
    MUTED = 3,
    ERROR = 4,
};

enum class HealthState : uint8_t {
    HEALTHY = 0,
    DEGRADED = 1,
    FAULT = 2,
    OFFLINE = 3,
};

enum class SafetyState : uint8_t {
    SAFE = 0,
    WARNING = 1,
    VIOLATION = 2,
    EMERGENCY_STOP = 3,
};

enum class SystemState : uint8_t {
    BOOTING = 0,
    READY = 1,
    RUNNING = 2,
    SHUTTING_DOWN = 3,
    ERROR = 4,
};

enum class LogLevel : uint8_t {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3,
    FATAL = 4,
};

enum class ErrorCode : uint8_t {
    NONE = 0,
    UNKNOWN = 1,
    I2C_BUS_ERROR = 10,
    SENSOR_TIMEOUT = 11,
    MOTOR_STALL = 12,
    SERVO_OUT_OF_BOUNDS = 13,
    BATTERY_LOW = 14,
    COMM_TIMEOUT = 15,
};

enum class SensorType : uint8_t {
    IMU = 0,
    ULTRASONIC = 1,
    LIDAR = 2,
    GAS = 3,
    CURRENT = 4,
};

#endif // ROVER_ENUMS_H
