/**
 * @file driver_hcsr04.cpp
 * @brief Recon Rover V1 - HC-SR04 Ultrasonic Sensor Driver
 *
 * Implementation of the DriverHcsr04 class.
 */

#include "driver_hcsr04.h"

namespace rover {
namespace driver {

DriverHcsr04::DriverHcsr04(gpio_num_t trig_pin, gpio_num_t echo_pin) 
    : m_trig(trig_pin), m_echo(echo_pin) {
}

hal::HalStatus DriverHcsr04::init() {
    hal::HalStatus st = m_trig.init(hal::GpioMode::OUTPUT, hal::GpioPull::NONE);
    if (!st.isOk()) return st;

    st = m_echo.init(hal::GpioMode::INPUT, hal::GpioPull::DOWN); // Pull down to prevent floating triggers
    if (!st.isOk()) return st;

    m_trig.write(false);
    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverHcsr04::measureDistanceCm(float& distance_cm, uint32_t timeout_us) {
    distance_cm = -1.0f;

    // Send 10us trigger pulse
    m_trig.write(true);
    hal::HalTimer::delayUs(10);
    m_trig.write(false);

    // Wait for echo to go HIGH
    uint64_t start_time = hal::HalTimer::getMicros();
    bool level = false;
    while (true) {
        m_echo.read(level);
        if (level) break; // Echo started
        
        if (hal::HalTimer::getMicros() - start_time > timeout_us) {
            return {hal::HalError::ERR_TIMEOUT, 0};
        }
    }

    // Echo is HIGH, start timing
    uint64_t echo_start = hal::HalTimer::getMicros();

    // Wait for echo to go LOW
    while (true) {
        m_echo.read(level);
        if (!level) break; // Echo ended
        
        if (hal::HalTimer::getMicros() - echo_start > timeout_us) {
            return {hal::HalError::ERR_TIMEOUT, 0};
        }
    }

    uint64_t echo_end = hal::HalTimer::getMicros();
    uint64_t pulse_duration = echo_end - echo_start;

    // Speed of sound is ~343 m/s, which is 0.0343 cm/us
    // Distance = (Duration * Speed) / 2
    distance_cm = (static_cast<float>(pulse_duration) * 0.0343f) / 2.0f;

    return {hal::HalError::OK, 0};
}

} // namespace driver
} // namespace rover
