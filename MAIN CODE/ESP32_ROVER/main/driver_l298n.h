/**
 * @file driver_l298n.h
 * @brief Recon Rover V1 - L298N Motor Driver
 *
 * Hardware driver for the L298N Dual H-Bridge.
 * Uses PWM on the IN1/IN2/IN3/IN4 pins to control speed and direction
 * without needing separate ENA/ENB pins.
 */

#ifndef ROVER_DRIVER_L298N_H
#define ROVER_DRIVER_L298N_H

#include "hal_ledc.h"
#include "driver/gpio.h"

namespace rover {
namespace driver {

/**
 * @class DriverL298N
 * @brief Driver class for the L298N motor controller.
 */
class DriverL298N {
public:
    /**
     * @brief Constructs the driver.
     * @param pwm Pointer to the LEDC HAL instance.
     * @param in1 Left motor forward pin.
     * @param in2 Left motor reverse pin.
     * @param in3 Right motor forward pin.
     * @param in4 Right motor reverse pin.
     */
    DriverL298N(hal::HalLedc* pwm, gpio_num_t in1, gpio_num_t in2, gpio_num_t in3, gpio_num_t in4);

    /**
     * @brief Initializes the PWM timers and channels.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Sets the speed and direction of the left motor.
     * @param speed Speed from -1.0 (full reverse) to 1.0 (full forward).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus setLeftSpeed(float speed);

    /**
     * @brief Sets the speed and direction of the right motor.
     * @param speed Speed from -1.0 (full reverse) to 1.0 (full forward).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus setRightSpeed(float speed);

    /**
     * @brief Stops both motors immediately (coast).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus stop();

    /**
     * @brief Actively brakes both motors (shorts motor terminals).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus brake();

private:
    hal::HalLedc* m_pwm;
    gpio_num_t m_in1;
    gpio_num_t m_in2;
    gpio_num_t m_in3;
    gpio_num_t m_in4;

    static constexpr uint32_t PWM_FREQ = 20000; // 20kHz
    static constexpr uint32_t PWM_MAX_DUTY = 8191; // 13-bit resolution

    hal::HalStatus setMotorPwm(ledc_channel_t ch_fwd, ledc_channel_t ch_rev, float speed);
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_L298N_H
