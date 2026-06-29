/**
 * @file hal_timer.h
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for Timers
 *
 * Provides a clean C++ interface for ESP32 hardware/software timers,
 * delays, and timestamp acquisition.
 */

#ifndef ROVER_HAL_TIMER_H
#define ROVER_HAL_TIMER_H

#include <cstdint>
#include "hal_types.h"
#include "esp_timer.h"

namespace rover {
namespace hal {

/**
 * @brief Type alias for periodic timer callbacks.
 * @param arg User-provided argument passed to the callback.
 */
using TimerCallback = void (*)(void* arg);

/**
 * @class HalTimer
 * @brief Hardware Abstraction Layer for general timing functionality.
 *
 * Provides static methods for timestamps/delays, and allows creation
 * of periodic software timers.
 */
class HalTimer {
public:
    /**
     * @brief Constructs an uninitialized periodic timer.
     */
    HalTimer();

    /**
     * @brief Destructor. Stops and deletes the timer if it was created.
     */
    ~HalTimer();

    /**
     * @brief Initializes a periodic timer.
     * @param callback The function to execute periodically.
     * @param arg Optional user argument for the callback.
     * @param name Optional name for the timer (used in debugging).
     * @return HalStatus indicating success or failure.
     */
    HalStatus initPeriodic(TimerCallback callback, void* arg = nullptr, const char* name = "rover_timer");

    /**
     * @brief Starts the periodic timer.
     * @param period_us The period between executions in microseconds.
     * @return HalStatus indicating success or failure.
     */
    HalStatus start(uint64_t period_us);

    /**
     * @brief Stops the periodic timer.
     * @return HalStatus indicating success or failure.
     */
    HalStatus stop();

    // =========================================================================
    // Global Utility Functions
    // =========================================================================

    /**
     * @brief Gets the number of microseconds since boot.
     * @return System uptime in microseconds.
     */
    static uint64_t getMicros();

    /**
     * @brief Gets the number of milliseconds since boot.
     * @return System uptime in milliseconds.
     */
    static uint32_t getMillis();

    /**
     * @brief Blocks execution for the specified number of milliseconds.
     * @note This yields to the FreeRTOS scheduler.
     * @param ms Milliseconds to delay.
     */
    static void delayMs(uint32_t ms);

    /**
     * @brief Blocks execution for the specified number of microseconds.
     * @note This uses a busy-wait loop for precise, short delays.
     *       Do not use for delays > 10ms.
     * @param us Microseconds to delay.
     */
    static void delayUs(uint32_t us);

private:
    esp_timer_handle_t m_timer_handle;  /**< The underlying ESP timer handle */
    bool m_initialized;                 /**< Tracks if the timer is initialized */
    bool m_running;                     /**< Tracks if the timer is currently running */
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_TIMER_H
