/**
 * @file messages.h
 * @brief Recon Rover V1 - Inter-Process Communication Messages
 *
 * Defines the event structures that will be passed through FreeRTOS
 * queues to communicate between Subsystem Managers.
 */

#ifndef ROVER_MESSAGES_H
#define ROVER_MESSAGES_H

#include "types_sensor.h"
#include "types_actuator.h"
#include "error_system.h"

namespace rover {

/**
 * @enum EventType
 * @brief Identifies the type of payload in a queue message.
 */
enum class EventType : uint8_t {
    SENSOR_IMU,
    SENSOR_TOF,
    SENSOR_SONAR,
    SENSOR_GAS,
    SENSOR_POWER,
    CMD_MOTOR,
    CMD_SERVO,
    CMD_EYE,
    CMD_LED,
    FAULT_RAISED,
    FAULT_CLEARED,
    SYSTEM_STATE_CHANGE
};

/**
 * @struct SensorEvent
 * @brief Carries new sensor data from SensorManager to TelemetryBuilder/HealthMonitor.
 */
struct SensorEvent {
    EventType type;
    union {
        IMUData imu;
        ToFData tof;
        UltrasonicData sonar;
        GasData gas;
        PowerData power;
    } data;
};

/**
 * @struct CommandEvent
 * @brief Carries parsed commands from CommandParser to Actuator Controllers.
 */
struct CommandEvent {
    EventType type;
    union {
        MotorCommand motor;
        ServoCommand servo;
        EyeCommand eye;
        LEDCommand led;
    } data;
};

/**
 * @struct FaultEvent
 * @brief Carries error information to the FaultManager.
 */
struct FaultEvent {
    EventType type;
    Error error;
};

/**
 * @struct SystemEvent
 * @brief Carries system-wide state changes (e.g., entering Safe Mode).
 */
struct SystemEvent {
    EventType type;
    uint8_t new_state; // Maps to SystemState enum
};

} // namespace rover

#endif // ROVER_MESSAGES_H
