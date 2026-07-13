/**
 * @file driver_servo.h
 * @brief Recon Rover V1 - Servo Motor Driver
 *
 * Hardware driver for standard 50Hz servos (like SG90).
 * Uses the LEDC PWM HAL.
 */

#ifndef ROVER_DRIVER_SERVO_H
#define ROVER_DRIVER_SERVO_H

#include "hal_ledc.h"

namespace rover {
namespace driver {

/**
 * @class DriverServo
 * @brief Driver class for a standard RC servo.
 */
class DriverServo {
public:
    /**
     * @brief Constructs the driver.
     * @param pwm Pointer to the LEDC HAL instance.
     * @param pin The GPIO pin for the servo signal.
     * @param channel The LEDC channel to use (4-7 recommended).
     */
    DriverServo(hal::HalLedc* pwm, gpio_num_t pin, ledc_channel_t channel);

    /**
     * @brief Initializes the PWM timer and channel for 50Hz operation.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Sets the servo angle.
     * @param angle_deg Angle in degrees (typically 0 to 180).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus setAngle(float angle_deg);

private:
    hal::HalLedc* m_pwm;
    gpio_num_t m_pin;
    ledc_channel_t m_channel;

    static constexpr uint32_t PWM_FREQ = 50; // 50 Hz
    static constexpr uint32_t PWM_MAX_DUTY = 65535; // 16-bit resolution
    
    // Pulse widths for SG90 (can be parameterized later)
    static constexpr float MIN_PULSE_MS = 0.5f;
    static constexpr float MAX_PULSE_MS = 2.4f;
    static constexpr float PERIOD_MS = 20.0f;
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_SERVO_H
