/**
 * @file watchdog_registry.cpp
 * @brief Recon Rover V1 - RTOS Watchdog Registry
 */

#include "watchdog_registry.h"

namespace rover {
namespace rtos {

WatchdogRegistry::WatchdogRegistry() {
    for (int i = 0; i < static_cast<int>(TaskId::MAX_TASKS); ++i) {
        m_records[i].active = false;
        m_records[i].timeout_ms = 0;
        m_records[i].last_checkin_ms = 0;
    }
}

WatchdogRegistry::~WatchdogRegistry() {}

void WatchdogRegistry::registerTask(TaskId id, uint32_t timeout_ms) {
    int idx = static_cast<int>(id);
    if (idx < static_cast<int>(TaskId::MAX_TASKS)) {
        m_records[idx].active = true;
        m_records[idx].timeout_ms = timeout_ms;
        // Assume checked in exactly at registration
        m_records[idx].last_checkin_ms = xTaskGetTickCount() * portTICK_PERIOD_MS;
    }
}

void WatchdogRegistry::checkIn(TaskId id) {
    int idx = static_cast<int>(id);
    if (idx < static_cast<int>(TaskId::MAX_TASKS) && m_records[idx].active) {
        m_records[idx].last_checkin_ms = xTaskGetTickCount() * portTICK_PERIOD_MS;
    }
}

bool WatchdogRegistry::checkAllTasks(uint32_t current_time_ms, TaskId& failed_task) {
    for (int i = 0; i < static_cast<int>(TaskId::MAX_TASKS); ++i) {
        if (m_records[i].active) {
            uint32_t elapsed = current_time_ms - m_records[i].last_checkin_ms;
            if (elapsed > m_records[i].timeout_ms) {
                failed_task = static_cast<TaskId>(i);
                return false; // Starvation detected
            }
        }
    }
    return true; // All healthy
}

} // namespace rtos
} // namespace rover
