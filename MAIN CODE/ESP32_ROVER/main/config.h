/**
 * @file config.h
 * @brief Recon Rover V1 - Global Configuration Constants
 *
 * Centralized repository for all hardware pins, timing configurations,
 * and system thresholds.
 */

#ifndef ROVER_CONFIG_H
#define ROVER_CONFIG_H

#include "driver/gpio.h"
#include <cstdint>

namespace rover {
namespace config {

// =========================================================================
// I2C Configuration
// =========================================================================
constexpr gpio_num_t I2C_SDA_PIN           = GPIO_NUM_4;
constexpr gpio_num_t I2C_SCL_PIN           = GPIO_NUM_5;
constexpr uint32_t   I2C_FREQ_HZ           = 400000;

// =========================================================================
// HC-SR04 Configuration
// =========================================================================
constexpr gpio_num_t HCSR04_TRIG_PIN       = GPIO_NUM_18;
constexpr gpio_num_t HCSR04_ECHO_PIN       = GPIO_NUM_19;

// =========================================================================
// Motor Configuration
// =========================================================================
constexpr gpio_num_t MOTOR_LEFT_IN1_PIN    = GPIO_NUM_25;
constexpr gpio_num_t MOTOR_LEFT_IN2_PIN    = GPIO_NUM_26;
constexpr gpio_num_t MOTOR_RIGHT_IN3_PIN   = GPIO_NUM_27;
constexpr gpio_num_t MOTOR_RIGHT_IN4_PIN   = GPIO_NUM_14;

// =========================================================================
// Servo Configuration
// =========================================================================
constexpr gpio_num_t SERVO_PAN_PIN         = GPIO_NUM_12;
constexpr gpio_num_t SERVO_TILT_PIN        = GPIO_NUM_13;

// =========================================================================
// LED Configuration
// =========================================================================
constexpr gpio_num_t WS2812B_PIN           = GPIO_NUM_21;
constexpr uint16_t   WS2812B_NUM_LEDS      = 8;

// =========================================================================
// Sensor Thresholds & Limits
// =========================================================================
constexpr int32_t    MQ2_HAZARD_THRESHOLD_MV = 2000; // 2.0V limit for gas
constexpr float      INA219_MAX_CURRENT_MA   = 2000.0f; 
constexpr float      INA219_MIN_BUS_VOLTAGE_V= 6.5f; // Low battery limit (2S LiPo)

// =========================================================================
// Timing Constants (in milliseconds)
// =========================================================================
constexpr uint32_t   POLL_RATE_IMU_MS      = 20;   // 50 Hz
constexpr uint32_t   POLL_RATE_TOF_MS      = 50;   // 20 Hz
constexpr uint32_t   POLL_RATE_SONAR_MS    = 100;  // 10 Hz
constexpr uint32_t   POLL_RATE_GAS_MS      = 500;  // 2 Hz
constexpr uint32_t   POLL_RATE_POWER_MS    = 1000; // 1 Hz
constexpr uint32_t   TELEMETRY_TX_RATE_MS  = 100;  // 10 Hz telemetry output

} // namespace config
} // namespace rover

#endif // ROVER_CONFIG_H
