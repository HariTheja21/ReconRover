/**
 * @file rtos_config.h
 * @brief Recon Rover V1 - FreeRTOS Configuration
 *
 * Defines task priorities, stack sizes, queue lengths, core affinities,
 * and execution periods for the entire RTOS framework.
 */

#ifndef ROVER_RTOS_CONFIG_H
#define ROVER_RTOS_CONFIG_H

#include <cstdint>

namespace rover {
namespace rtos {

// =========================================================================
// CPU Core Affinities
// =========================================================================
constexpr int CORE_0 = 0; // Protocol, Display, Health, Watchdog
constexpr int CORE_1 = 1; // Real-time control (Sensors, Motors, Servos)
constexpr int CORE_ANY = -1;

// =========================================================================
// Task Priorities (0 is lowest, 24 is max in ESP-IDF typical config)
// =========================================================================
constexpr uint32_t PRIORITY_WATCHDOG    = 10;
constexpr uint32_t PRIORITY_FAULT       = 9;
constexpr uint32_t PRIORITY_MOTOR       = 9;
constexpr uint32_t PRIORITY_SERIAL      = 8;
constexpr uint32_t PRIORITY_SENSOR      = 7;
constexpr uint32_t PRIORITY_SERVO       = 6;
constexpr uint32_t PRIORITY_TELEMETRY   = 5;
constexpr uint32_t PRIORITY_HEALTH      = 5;
constexpr uint32_t PRIORITY_OLED        = 4;
constexpr uint32_t PRIORITY_LED         = 4;

// =========================================================================
// Task Stack Sizes (in Bytes)
// =========================================================================
constexpr uint32_t STACK_WATCHDOG       = 2048;
constexpr uint32_t STACK_FAULT          = 2048;
constexpr uint32_t STACK_MOTOR          = 3072;
constexpr uint32_t STACK_SERIAL         = 4096; // Needs JSON parsing space
constexpr uint32_t STACK_SENSOR         = 4096; // I2C, floating point math
constexpr uint32_t STACK_SERVO          = 2048;
constexpr uint32_t STACK_TELEMETRY      = 4096; // Needs JSON formatting space
constexpr uint32_t STACK_HEALTH         = 2048;
constexpr uint32_t STACK_OLED           = 3072; // Frame buffer manipulation
constexpr uint32_t STACK_LED            = 2048;

// =========================================================================
// Queue Lengths (Number of items)
// =========================================================================
constexpr uint32_t Q_LEN_SENSOR         = 20;
constexpr uint32_t Q_LEN_TELEMETRY      = 20;
constexpr uint32_t Q_LEN_COMMAND        = 10;
constexpr uint32_t Q_LEN_MOTOR          = 10;
constexpr uint32_t Q_LEN_SERVO          = 5;
constexpr uint32_t Q_LEN_OLED           = 5;
constexpr uint32_t Q_LEN_LED            = 5;
constexpr uint32_t Q_LEN_HEALTH         = 10;
constexpr uint32_t Q_LEN_FAULT          = 10;
constexpr uint32_t Q_LEN_SYSTEM         = 5;

// =========================================================================
// Execution Periods / Delays (in ms)
// =========================================================================
constexpr uint32_t PERIOD_WATCHDOG_MS   = 10;
constexpr uint32_t PERIOD_SENSOR_MS     = 20;
constexpr uint32_t PERIOD_SERIAL_MS     = 10;
constexpr uint32_t PERIOD_MOTOR_MS      = 20;
constexpr uint32_t PERIOD_SERVO_MS      = 50;
constexpr uint32_t PERIOD_OLED_MS       = 100;
constexpr uint32_t PERIOD_LED_MS        = 50;
constexpr uint32_t PERIOD_TELEMETRY_MS  = 100;
constexpr uint32_t PERIOD_HEALTH_MS     = 1000;

} // namespace rtos
} // namespace rover

#endif // ROVER_RTOS_CONFIG_H
