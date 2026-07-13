/**
 * @file sync_manager.h
 * @brief Recon Rover V1 - RTOS Synchronization Manager
 *
 * Encapsulates FreeRTOS synchronization primitives (Mutexes, 
 * Event Groups) to avoid leaking RTOS headers into application logic.
 */

#ifndef ROVER_SYNC_MANAGER_H
#define ROVER_SYNC_MANAGER_H

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/event_groups.h"
#include <cstdint>

namespace rover {
namespace rtos {

/**
 * @class Mutex
 * @brief A standard FreeRTOS mutex wrapper.
 */
class Mutex {
public:
    Mutex();
    ~Mutex();

    bool init();
    bool lock(uint32_t wait_ms = portMAX_DELAY);
    bool unlock();

private:
    SemaphoreHandle_t m_handle;
};

/**
 * @class RecursiveMutex
 * @brief A FreeRTOS recursive mutex wrapper.
 */
class RecursiveMutex {
public:
    RecursiveMutex();
    ~RecursiveMutex();

    bool init();
    bool lock(uint32_t wait_ms = portMAX_DELAY);
    bool unlock();

private:
    SemaphoreHandle_t m_handle;
};

/**
 * @class EventGroup
 * @brief A FreeRTOS Event Group wrapper.
 */
class EventGroup {
public:
    EventGroup();
    ~EventGroup();

    bool init();
    
    void setBits(uint32_t bits);
    void clearBits(uint32_t bits);
    uint32_t waitBits(uint32_t bits, bool clear_on_exit, bool wait_for_all, uint32_t wait_ms = portMAX_DELAY);

private:
    EventGroupHandle_t m_handle;
};

} // namespace rtos
} // namespace rover

#endif // ROVER_SYNC_MANAGER_H
