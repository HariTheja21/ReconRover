/**
 * @file system_clock.cpp
 * @brief Recon Rover V1 - RTOS System Clock
 */

#include "system_clock.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

namespace rover {
namespace rtos {

uint32_t SystemClock::millis() {
    return static_cast<uint32_t>(esp_timer_get_time() / 1000ULL);
}

uint64_t SystemClock::micros() {
    return static_cast<uint64_t>(esp_timer_get_time());
}

void SystemClock::delayMs(uint32_t ms) {
    vTaskDelay(pdMS_TO_TICKS(ms));
}

} // namespace rtos
} // namespace rover
