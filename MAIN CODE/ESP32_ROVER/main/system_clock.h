/**
 * @file system_clock.h
 * @brief Recon Rover V1 - RTOS System Clock
 *
 * Provides RTOS-aware timekeeping and delay functions.
 */

#ifndef ROVER_SYSTEM_CLOCK_H
#define ROVER_SYSTEM_CLOCK_H

#include <cstdint>

namespace rover {
namespace rtos {

/**
 * @class SystemClock
 * @brief Singleton-like timekeeping utility.
 */
class SystemClock {
public:
    /**
     * @brief Gets the uptime in milliseconds since boot.
     * @return Uptime in ms.
     */
    static uint32_t millis();

    /**
     * @brief Gets the uptime in microseconds since boot.
     * @return Uptime in us.
     */
    static uint64_t micros();

    /**
     * @brief Blocks the current RTOS task for a specified duration.
     * @param ms Delay duration in milliseconds.
     */
    static void delayMs(uint32_t ms);
};

} // namespace rtos
} // namespace rover

#endif // ROVER_SYSTEM_CLOCK_H
