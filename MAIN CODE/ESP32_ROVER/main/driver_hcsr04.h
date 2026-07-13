/**
 * @file driver_hcsr04.h
 * @brief Recon Rover V1 - HC-SR04 Ultrasonic Sensor Driver
 *
 * Hardware driver for the HC-SR04 ultrasonic distance sensor.
 * Handles triggering the pulse and measuring the echo via busy-wait timing.
 */

#ifndef ROVER_DRIVER_HCSR04_H
#define ROVER_DRIVER_HCSR04_H

#include <cstdint>
#include "hal_gpio.h"
#include "hal_timer.h"

namespace rover {
namespace driver {

/**
 * @class DriverHcsr04
 * @brief Driver class for the HC-SR04.
 */
class DriverHcsr04 {
public:
    /**
     * @brief Constructs the driver.
     * @param trig_pin The GPIO pin used to trigger the sensor.
     * @param echo_pin The GPIO pin used to read the echo.
     */
    DriverHcsr04(gpio_num_t trig_pin, gpio_num_t echo_pin);

    /**
     * @brief Initializes the GPIO pins for the sensor.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Measures the distance in centimeters.
     * Generates a 10us trigger pulse and measures the echo length.
     * @param[out] distance_cm The calculated distance in centimeters.
     * @param timeout_us The maximum time to wait for the echo (limits range, prevents lockup).
     * @return HalStatus indicating success (OK) or failure (ERR_TIMEOUT).
     */
    hal::HalStatus measureDistanceCm(float& distance_cm, uint32_t timeout_us = 30000);

private:
    hal::HalGpio m_trig; /**< HAL wrapper for trigger pin */
    hal::HalGpio m_echo; /**< HAL wrapper for echo pin */
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_HCSR04_H
