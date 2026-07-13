/**
 * @file hal_timer.cpp
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for Timers
 *
 * Implementation of the HalTimer class and global utility functions.
 */

#include "hal_timer.h"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include "esp_rom_sys.h" // For esp_rom_delay_us

namespace rover {
namespace hal {

HalTimer::HalTimer() : m_timer_handle(nullptr), m_initialized(false), m_running(false) {
}

HalTimer::~HalTimer() {
    if (m_running) {
        stop();
    }
    if (m_initialized && m_timer_handle != nullptr) {
        esp_timer_delete(m_timer_handle);
    }
}

HalStatus HalTimer::initPeriodic(TimerCallback callback, void* arg, const char* name) {
    if (m_initialized) {
        return {HalError::ERR_ALREADY_INITIALIZED, ESP_OK};
    }
    if (callback == nullptr) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    esp_timer_create_args_t timer_args = {};
    timer_args.callback = callback;
    timer_args.arg = arg;
    timer_args.dispatch_method = ESP_TIMER_TASK; // Run in ESP timer task
    timer_args.name = name;
    timer_args.skip_unhandled_events = true;

    esp_err_t err = esp_timer_create(&timer_args, &m_timer_handle);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    m_initialized = true;
    return {HalError::OK, ESP_OK};
}

HalStatus HalTimer::start(uint64_t period_us) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (m_running) {
        return {HalError::OK, ESP_OK}; // Already running
    }

    esp_err_t err = esp_timer_start_periodic(m_timer_handle, period_us);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    m_running = true;
    return {HalError::OK, ESP_OK};
}

HalStatus HalTimer::stop() {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (!m_running) {
        return {HalError::OK, ESP_OK}; // Already stopped
    }

    esp_err_t err = esp_timer_stop(m_timer_handle);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    m_running = false;
    return {HalError::OK, ESP_OK};
}

// =========================================================================
// Global Utility Functions
// =========================================================================

uint64_t HalTimer::getMicros() {
    return static_cast<uint64_t>(esp_timer_get_time());
}

uint32_t HalTimer::getMillis() {
    return static_cast<uint32_t>(esp_timer_get_time() / 1000ULL);
}

void HalTimer::delayMs(uint32_t ms) {
    vTaskDelay(pdMS_TO_TICKS(ms));
}

void HalTimer::delayUs(uint32_t us) {
    // esp_rom_delay_us is a busy-wait loop, which is accurate for microseconds
    esp_rom_delay_us(us);
}

} // namespace hal
} // namespace rover
