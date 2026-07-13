/**
 * @file driver_servo.cpp
 * @brief Recon Rover V1 - Servo Motor Driver
 *
 * Implementation of the DriverServo class.
 */

#include "driver_servo.h"
#include "utils.h"

namespace rover {
namespace driver {

DriverServo::DriverServo(hal::HalLedc* pwm, gpio_num_t pin, ledc_channel_t channel)
    : m_pwm(pwm), m_pin(pin), m_channel(channel) {
}

hal::HalStatus DriverServo::init() {
    if (m_pwm == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    // Configure Timer 1 for servos
    hal::LedcTimerConfig timer_cfg = {};
    timer_cfg.timer_num = LEDC_TIMER_1;
    timer_cfg.speed_mode = LEDC_LOW_SPEED_MODE;
    timer_cfg.freq_hz = PWM_FREQ;
    timer_cfg.duty_resolution = LEDC_TIMER_16_BIT;
    
    // We assume Timer 1 is shared among all servos. Calling configTimer multiple times
    // is safe as long as the config is identical.
    hal::HalStatus st = m_pwm->configTimer(timer_cfg);
    if (!st.isOk()) return st;

    // Configure the specific channel
    hal::LedcChannelConfig ch_cfg = {};
    ch_cfg.timer_num = LEDC_TIMER_1;
    ch_cfg.speed_mode = LEDC_LOW_SPEED_MODE;
    ch_cfg.channel = m_channel;
    ch_cfg.pin = m_pin;
    
    return m_pwm->configChannel(ch_cfg);
}

hal::HalStatus DriverServo::setAngle(float angle_deg) {
    angle_deg = utils::constrainFloat(angle_deg, 0.0f, 180.0f);
    
    float target_pulse_ms = utils::mapFloat(angle_deg, 0.0f, 180.0f, MIN_PULSE_MS, MAX_PULSE_MS);
    
    uint32_t duty = static_cast<uint32_t>((target_pulse_ms / PERIOD_MS) * static_cast<float>(PWM_MAX_DUTY));
    
    return m_pwm->setDuty(m_channel, LEDC_LOW_SPEED_MODE, duty);
}

} // namespace driver
} // namespace rover
