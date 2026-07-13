/**
 * @file types_protocol.h
 * @brief Recon Rover V1 - Common Protocol Types
 *
 * Defines the cross-module protocol structures used to build
 * and parse the JSON packets between the ESP32 and Raspberry Pi.
 */

#ifndef ROVER_TYPES_PROTOCOL_H
#define ROVER_TYPES_PROTOCOL_H

#include <cstdint>
#include "types_sensor.h"
#include "types_actuator.h"

namespace rover {

/**
 * @enum SystemState
 * @brief High-level state of the ESP32 firmware.
 */
enum class SystemState : uint8_t {
    BOOTING = 0,
    IDLE,
    ACTIVE,
    SAFE_MODE,
    FAULT
};

/**
 * @struct TelemetryPacket
 * @brief Aggregated state of the robot, sent from ESP32 to Pi.
 * Note: This struct represents the logical data model, not the 
 * final serialized JSON or byte buffer.
 */
struct TelemetryPacket {
    uint32_t timestamp_ms;    /**< ESP32 uptime in milliseconds */
    SystemState state;        /**< Current system state */
    
    IMUData imu;              /**< Latest IMU readings */
    ToFData tof;              /**< Latest ToF reading */
    UltrasonicData sonar;     /**< Latest Ultrasonic reading */
    GasData gas;              /**< Latest Gas reading */
    PowerData power;          /**< Latest Power reading */
    
    uint32_t active_faults;   /**< Bitmask of currently active faults */
};

/**
 * @struct CommandPacket
 * @brief Directives sent from the Pi to the ESP32.
 * Note: This struct represents the logical data model parsed from JSON.
 */
struct CommandPacket {
    uint32_t sequence_num;    /**< Packet sequence number for tracking */
    
    bool has_motor_cmd;       /**< True if motor_cmd is populated */
    MotorCommand motor_cmd;
    
    bool has_servo_cmd;       /**< True if servo_cmd is populated */
    ServoCommand servo_cmd;
    
    bool has_eye_cmd;         /**< True if eye_cmd is populated */
    EyeCommand eye_cmd;
    
    bool has_led_cmd;         /**< True if led_cmd is populated */
    LEDCommand led_cmd;
};

} // namespace rover

#endif // ROVER_TYPES_PROTOCOL_H
