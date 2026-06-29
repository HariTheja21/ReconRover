/**
 * @file hal_ledc.h
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for LEDC (PWM)
 *
 * Provides a clean C++ interface for ESP32 LEDC PWM peripheral, useful for
 * motor speed control and servo angle control.
 */

#ifndef ROVER_HAL_LEDC_H
#define ROVER_HAL_LEDC_H

#include <cstdint>
#include "hal_types.h"
#include "driver/ledc.h"

namespace rover {
namespace hal {

/**
 * @struct LedcTimerConfig
 * @brief Configuration for an LEDC Timer.
 */
struct LedcTimerConfig {
    ledc_timer_t timer_num;         /**< Timer index */
    ledc_mode_t speed_mode;         /**< Speed mode (high/low speed) */
    uint32_t freq_hz;               /**< PWM frequency in Hz */
    ledc_timer_bit_t duty_resolution; /**< PWM duty resolution (bits) */
};

/**
 * @struct LedcChannelConfig
 * @brief Configuration for an LEDC Channel.
 */
struct LedcChannelConfig {
    ledc_channel_t channel;         /**< Channel index */
    gpio_num_t pin;                 /**< GPIO pin to output PWM */
    ledc_timer_t timer_num;         /**< Timer index to associate with */
    ledc_mode_t speed_mode;         /**< Speed mode (must match timer) */
};

/**
 * @class HalLedc
 * @brief Hardware Abstraction Layer for the ESP32 LEDC (PWM) peripheral.
 *
 * Manages timer and channel configuration, and allows updating the duty cycle.
 */
class HalLedc {
public:
    /**
     * @brief Constructs a new HalLedc object.
     */
    HalLedc();

    /**
     * @brief Destructor. Stops PWM and releases resources.
     */
    ~HalLedc();

    /**
     * @brief Configures a PWM timer. Multiple channels can share a timer.
     * @param config The timer configuration.
     * @return HalStatus indicating success or failure.
     */
    HalStatus configTimer(const LedcTimerConfig& config);

    /**
     * @brief Configures a PWM channel and links it to a timer and GPIO pin.
     * @param config The channel configuration.
     * @return HalStatus indicating success or failure.
     */
    HalStatus configChannel(const LedcChannelConfig& config);

    /**
     * @brief Updates the duty cycle for a specific channel.
     * @param channel The channel to update.
     * @param speed_mode The speed mode of the channel.
     * @param duty_val The new duty cycle value (scaled according to configured bit resolution).
     * @return HalStatus indicating success or failure.
     */
    HalStatus setDuty(ledc_channel_t channel, ledc_mode_t speed_mode, uint32_t duty_val);

    /**
     * @brief Stops PWM output on a specific channel, driving the pin to a given idle level.
     * @param channel The channel to stop.
     * @param speed_mode The speed mode of the channel.
     * @param idle_level The logic level to hold the pin at (0 or 1).
     * @return HalStatus indicating success or failure.
     */
    HalStatus stop(ledc_channel_t channel, ledc_mode_t speed_mode, uint32_t idle_level);

private:
    bool m_timer_configured;   /**< Tracks if a timer has been configured */
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_LEDC_H
