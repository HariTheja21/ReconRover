/**
 * @file hal_ledc.cpp
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for LEDC (PWM)
 *
 * Implementation of the HalLedc class.
 */

#include "hal_ledc.h"

namespace rover {
namespace hal {

HalLedc::HalLedc() : m_timer_configured(false) {
}

HalLedc::~HalLedc() {
    // LEDC resource de-initialization relies on overwriting configs or
    // calling ledc_stop. Individual channels should be stopped explicitly.
}

HalStatus HalLedc::configTimer(const LedcTimerConfig& config) {
    ledc_timer_config_t timer_conf = {};
    timer_conf.speed_mode = config.speed_mode;
    timer_conf.timer_num = config.timer_num;
    timer_conf.duty_resolution = config.duty_resolution;
    timer_conf.freq_hz = config.freq_hz;
    timer_conf.clk_cfg = LEDC_AUTO_CLK;

    esp_err_t err = ledc_timer_config(&timer_conf);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    m_timer_configured = true;
    return {HalError::OK, ESP_OK};
}

HalStatus HalLedc::configChannel(const LedcChannelConfig& config) {
    if (!m_timer_configured) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }

    ledc_channel_config_t channel_conf = {};
    channel_conf.channel = config.channel;
    channel_conf.duty = 0;
    channel_conf.gpio_num = config.pin;
    channel_conf.speed_mode = config.speed_mode;
    channel_conf.hpoint = 0;
    channel_conf.timer_sel = config.timer_num;
    channel_conf.intr_type = LEDC_INTR_DISABLE;

    esp_err_t err = ledc_channel_config(&channel_conf);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    return {HalError::OK, ESP_OK};
}

HalStatus HalLedc::setDuty(ledc_channel_t channel, ledc_mode_t speed_mode, uint32_t duty_val) {
    esp_err_t err = ledc_set_duty(speed_mode, channel, duty_val);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    err = ledc_update_duty(speed_mode, channel);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    return {HalError::OK, ESP_OK};
}

HalStatus HalLedc::stop(ledc_channel_t channel, ledc_mode_t speed_mode, uint32_t idle_level) {
    esp_err_t err = ledc_stop(speed_mode, channel, idle_level);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }
    return {HalError::OK, ESP_OK};
}

} // namespace hal
} // namespace rover
