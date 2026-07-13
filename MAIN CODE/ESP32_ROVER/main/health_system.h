/**
 * @file health_system.h
 * @brief Recon Rover V1 - Centralized Health Tracking
 *
 * Defines structures for tracking the uptime and fault status of various
 * hardware and software subsystems.
 */

#ifndef ROVER_HEALTH_SYSTEM_H
#define ROVER_HEALTH_SYSTEM_H

#include <cstdint>

namespace rover {

/**
 * @struct DeviceHealth
 * @brief Generic health tracker for a single hardware device.
 */
struct DeviceHealth {
    bool is_online;           /**< True if the device passed its last health check */
    uint32_t failure_count;   /**< Number of times the device has failed a check */
    uint32_t last_check_ms;   /**< Timestamp of the last health check */
};

/**
 * @struct SensorHealth
 * @brief Aggregates the health of all sensor hardware.
 */
struct SensorHealth {
    DeviceHealth mpu6050;
    DeviceHealth vl53l0x;
    DeviceHealth hcsr04;
    DeviceHealth mq2;
    DeviceHealth pca9548a;
};

/**
 * @struct CommunicationHealth
 * @brief Tracks the health of the USB CDC link.
 */
struct CommunicationHealth {
    bool is_connected;        /**< True if a DTR signal is asserted by host */
    uint32_t packets_rx;      /**< Total command packets received */
    uint32_t packets_tx;      /**< Total telemetry packets sent */
    uint32_t parse_errors;    /**< Number of JSON parse errors */
    uint32_t crc_errors;      /**< Number of CRC mismatches */
};

/**
 * @struct PowerHealth
 * @brief Tracks battery and power monitor status.
 */
struct PowerHealth {
    DeviceHealth ina219;
    bool battery_low;         /**< True if bus voltage drops below MIN_BUS_VOLTAGE_V */
    bool overcurrent;         /**< True if load current exceeds MAX_CURRENT_MA */
};

/**
 * @struct SystemHealth
 * @brief Top-level aggregate health of the entire firmware.
 */
struct SystemHealth {
    uint32_t uptime_ms;
    uint32_t free_heap_bytes;
    SensorHealth sensors;
    CommunicationHealth comms;
    PowerHealth power;
    bool safe_mode_active;    /**< True if the system has entered safe mode due to a fault */
};

} // namespace rover

#endif // ROVER_HEALTH_SYSTEM_H
