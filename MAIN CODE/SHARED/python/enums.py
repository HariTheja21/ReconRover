# AUTO-GENERATED FILE. DO NOT MODIFY.
from enum import Enum, IntEnum

class OperatingMode(IntEnum):
    STANDBY = 0
    REMOTE = 1
    SMART_CONTROL = 2
    LEGEND_AI = 3
    EMERGENCY = 99

class MissionMode(IntEnum):
    IDLE = 0
    OBSTACLE_AVOIDANCE = 1
    EXPLORATION = 2
    PERSON_FOLLOWING = 3
    OBJECT_FOLLOWING = 4
    MOTION_DETECTION = 5
    SCENE_EXPLANATION = 6
    HOME_ASSISTANT = 7
    DIAGNOSTICS = 8
    CALIBRATION = 9

class CommandType(IntEnum):
    MOTION = 10
    SERVO = 11
    LED = 12
    OLED = 13
    CAMERA = 14
    AUDIO = 15
    SYSTEM = 16
    MISSION = 17
    CONFIG = 18

class TelemetryType(IntEnum):
    HEARTBEAT = 20
    SYSTEM_HEALTH = 21
    BATTERY = 22
    IMU = 23
    DISTANCE = 24
    ENVIRONMENT = 25
    MOTOR_STATUS = 26
    SERVO_STATUS = 27
    LOG_MESSAGE = 28

class EventType(IntEnum):
    SYSTEM_STARTUP = 100
    SYSTEM_SHUTDOWN = 101
    MODE_CHANGED = 102
    MISSION_CHANGED = 103
    CONFIG_CHANGED = 104
    HARDWARE_FAULT = 105
    SENSOR_READING = 106
    AI_INFERENCE = 107

class ConnectionState(IntEnum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    ERROR = 3

class BatteryState(IntEnum):
    FULL = 0
    NORMAL = 1
    WARNING = 2
    CRITICAL = 3
    CHARGING = 4

class MotorState(IntEnum):
    STOPPED = 0
    MOVING_FORWARD = 1
    MOVING_REVERSE = 2
    TURNING = 3
    FAULT = 4

class ServoState(IntEnum):
    IDLE = 0
    MOVING = 1
    STALLED = 2
    ERROR = 3

class CameraState(IntEnum):
    OFF = 0
    STREAMING = 1
    RECORDING = 2
    ERROR = 3

class LEDState(IntEnum):
    OFF = 0
    SOLID = 1
    BLINKING = 2
    PULSING = 3
    RAINBOW = 4

class VoiceState(IntEnum):
    LISTENING = 0
    PROCESSING = 1
    SPEAKING = 2
    MUTED = 3
    ERROR = 4

class HealthState(IntEnum):
    HEALTHY = 0
    DEGRADED = 1
    FAULT = 2
    OFFLINE = 3

class SafetyState(IntEnum):
    SAFE = 0
    WARNING = 1
    VIOLATION = 2
    EMERGENCY_STOP = 3

class SystemState(IntEnum):
    BOOTING = 0
    READY = 1
    RUNNING = 2
    SHUTTING_DOWN = 3
    ERROR = 4

class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4

class ErrorCode(IntEnum):
    NONE = 0
    UNKNOWN = 1
    I2C_BUS_ERROR = 10
    SENSOR_TIMEOUT = 11
    MOTOR_STALL = 12
    SERVO_OUT_OF_BOUNDS = 13
    BATTERY_LOW = 14
    COMM_TIMEOUT = 15

class SensorType(IntEnum):
    IMU = 0
    ULTRASONIC = 1
    LIDAR = 2
    GAS = 3
    CURRENT = 4

