/**
 * @file driver_l298n.cpp
 * @brief Recon Rover V1 - L298N Motor Driver
 *
 * Implementation of the DriverL298N class.
 */

#include "driver_l298n.h"
#include "utils.h"

namespace rover {
namespace driver {

DriverL298N::DriverL298N(hal::HalLedc* pwm, gpio_num_t in1, gpio_num_t in2, gpio_num_t in3, gpio_num_t in4)
    : m_pwm(pwm), m_in1(in1), m_in2(in2), m_in3(in3), m_in4(in4) {
}

hal::HalStatus DriverL298N::init() {
    if (m_pwm == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    // Configure Timer 0 for all 4 motor PWM channels
    hal::LedcTimerConfig timer_cfg = {};
    timer_cfg.timer_num = LEDC_TIMER_0;
    timer_cfg.speed_mode = LEDC_LOW_SPEED_MODE;
    timer_cfg.freq_hz = PWM_FREQ;
    timer_cfg.duty_resolution = LEDC_TIMER_13_BIT;
    
    hal::HalStatus st = m_pwm->configTimer(timer_cfg);
    if (!st.isOk()) return st;

    // Configure 4 channels
    hal::LedcChannelConfig ch_cfg = {};
    ch_cfg.timer_num = LEDC_TIMER_0;
    ch_cfg.speed_mode = LEDC_LOW_SPEED_MODE;

    ch_cfg.channel = LEDC_CHANNEL_0; ch_cfg.pin = m_in1;
    st = m_pwm->configChannel(ch_cfg);
    if (!st.isOk()) return st;

    ch_cfg.channel = LEDC_CHANNEL_1; ch_cfg.pin = m_in2;
    st = m_pwm->configChannel(ch_cfg);
    if (!st.isOk()) return st;

    ch_cfg.channel = LEDC_CHANNEL_2; ch_cfg.pin = m_in3;
    st = m_pwm->configChannel(ch_cfg);
    if (!st.isOk()) return st;

    ch_cfg.channel = LEDC_CHANNEL_3; ch_cfg.pin = m_in4;
    return m_pwm->configChannel(ch_cfg);
}

hal::HalStatus DriverL298N::setMotorPwm(ledc_channel_t ch_fwd, ledc_channel_t ch_rev, float speed) {
    speed = utils::constrainFloat(speed, -1.0f, 1.0f);
    
    uint32_t duty = static_cast<uint32_t>(utils::mapFloat(std::abs(speed), 0.0f, 1.0f, 0.0f, static_cast<float>(PWM_MAX_DUTY)));

    hal::HalStatus st;
    if (speed > 0.01f) {
        st = m_pwm->setDuty(ch_fwd, LEDC_LOW_SPEED_MODE, duty);
        if (!st.isOk()) return st;
        st = m_pwm->setDuty(ch_rev, LEDC_LOW_SPEED_MODE, 0);
    } else if (speed < -0.01f) {
        st = m_pwm->setDuty(ch_fwd, LEDC_LOW_SPEED_MODE, 0);
        if (!st.isOk()) return st;
        st = m_pwm->setDuty(ch_rev, LEDC_LOW_SPEED_MODE, duty);
    } else {
        st = m_pwm->setDuty(ch_fwd, LEDC_LOW_SPEED_MODE, 0);
        if (!st.isOk()) return st;
        st = m_pwm->setDuty(ch_rev, LEDC_LOW_SPEED_MODE, 0);
    }
    return st;
}

hal::HalStatus DriverL298N::setLeftSpeed(float speed) {
    return setMotorPwm(LEDC_CHANNEL_0, LEDC_CHANNEL_1, speed);
}

hal::HalStatus DriverL298N::setRightSpeed(float speed) {
    return setMotorPwm(LEDC_CHANNEL_2, LEDC_CHANNEL_3, speed);
}

hal::HalStatus DriverL298N::stop() {
    hal::HalStatus st = setLeftSpeed(0.0f);
    if (!st.isOk()) return st;
    return setRightSpeed(0.0f);
}

hal::HalStatus DriverL298N::brake() {
    // Setting both IN1 and IN2 HIGH applies active braking in L298N
    hal::HalStatus st = m_pwm->setDuty(LEDC_CHANNEL_0, LEDC_LOW_SPEED_MODE, PWM_MAX_DUTY);
    st = m_pwm->setDuty(LEDC_CHANNEL_1, LEDC_LOW_SPEED_MODE, PWM_MAX_DUTY);
    st = m_pwm->setDuty(LEDC_CHANNEL_2, LEDC_LOW_SPEED_MODE, PWM_MAX_DUTY);
    st = m_pwm->setDuty(LEDC_CHANNEL_3, LEDC_LOW_SPEED_MODE, PWM_MAX_DUTY);
    return st;
}

} // namespace driver
} // namespace rover
