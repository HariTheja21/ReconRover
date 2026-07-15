// AUTO-GENERATED FILE. DO NOT MODIFY.
#ifndef ROVER_CONSTANTS_H
#define ROVER_CONSTANTS_H

#include <stdint.h>

namespace SystemConstants {
    constexpr const char* FIRMWARE_VERSION = "2.0.0";
    constexpr uint8_t PROTOCOL_VERSION = 2;
    constexpr uint8_t MAX_MODULES = 32;
    constexpr uint16_t DEFAULT_TICK_RATE_HZ = 50;
    constexpr const char* ROBOT_NAME = "Recon Rover V2";
    constexpr const char* HARDWARE_REVISION = "RevB";
}

namespace CommunicationConstants {
    constexpr uint32_t BAUD_RATE = 115200;
    constexpr uint16_t MAX_PACKET_SIZE = 256;
    constexpr uint8_t SYNC_BYTE_1 = 0xAA;
    constexpr uint8_t SYNC_BYTE_2 = 0x55;
    constexpr uint16_t TELEMETRY_PORT = 5000;
    constexpr uint16_t COMMAND_PORT = 5001;
}

namespace SafetyConstants {
    constexpr float CRITICAL_BATTERY_V = 6.8f;
    constexpr float WARNING_BATTERY_V = 7.2f;
    constexpr uint16_t MAX_MOTOR_CURRENT_MA = 2000;
    constexpr float EMERGENCY_STOP_DISTANCE_CM = 15.0f;
    constexpr uint32_t COMM_TIMEOUT_MS = 1000;
}

namespace MotionConstants {
    constexpr uint8_t MIN_PWM = 0;
    constexpr uint8_t MAX_PWM = 255;
    constexpr uint8_t DEFAULT_SPEED = 150;
    constexpr uint8_t TURN_SPEED = 180;
    constexpr uint8_t ACCEL_STEP = 10;
}

namespace ServoConstants {
    constexpr uint8_t PAN_MIN = 0;
    constexpr uint8_t PAN_MAX = 180;
    constexpr uint8_t PAN_CENTER = 90;
    constexpr uint8_t TILT_MIN = 30;
    constexpr uint8_t TILT_MAX = 150;
    constexpr uint8_t TILT_CENTER = 90;
    constexpr uint8_t DEFAULT_SPEED = 50;
}

namespace SensorsConstants {
    constexpr uint8_t MPU6050_ADDR = 0x68; // Decimal 104
    constexpr uint8_t VL53L0X_ADDR = 0x29; // Decimal 41
    constexpr uint8_t INA219_ADDR = 0x40;  // Decimal 64
    constexpr uint8_t PCA9548A_ADDR = 0x70; // Decimal 112
}

namespace DeveloperConstants {
    constexpr bool DEBUG_MODE_ENABLED = true;
    constexpr bool VERBOSE_SERIAL_LOGGING = false;
    constexpr uint32_t HEARTBEAT_INTERVAL_MS = 1000;
}

#endif // ROVER_CONSTANTS_H
