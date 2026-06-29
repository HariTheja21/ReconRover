/**
 * @file watchdog_registry.h
 * @brief Recon Rover V1 - RTOS Watchdog Registry
 *
 * Provides a registration interface for tasks to check-in with the 
 * system watchdog.
 */

#ifndef ROVER_WATCHDOG_REGISTRY_H
#define ROVER_WATCHDOG_REGISTRY_H

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <cstdint>

namespace rover {
namespace rtos {

/**
 * @enum TaskId
 * @brief Identifiers for tasks that need watchdog monitoring.
 */
enum class TaskId : uint8_t {
    SERIAL = 0,
    MOTOR,
    SENSOR,
    SERVO,
    OLED,
    LED,
    TELEMETRY,
    HEALTH,
    MAX_TASKS
};

/**
 * @class WatchdogRegistry
 * @brief Tracks which tasks have checked in.
 */
class WatchdogRegistry {
public:
    WatchdogRegistry();
    ~WatchdogRegistry();

    /**
     * @brief Registers the calling task for monitoring.
     * @param id The logical ID of the task.
     * @param timeout_ms The maximum time allowed between check-ins.
     */
    void registerTask(TaskId id, uint32_t timeout_ms);

    /**
     * @brief Feeds the watchdog for a specific task.
     * @param id The logical ID of the task.
     */
    void checkIn(TaskId id);

    /**
     * @brief Checks if any task has exceeded its timeout.
     * @param current_time_ms The current system time.
     * @param[out] failed_task The ID of the task that failed, if any.
     * @return True if all tasks are healthy, False if a task is starved.
     */
    bool checkAllTasks(uint32_t current_time_ms, TaskId& failed_task);

private:
    struct TaskRecord {
        bool active;
        uint32_t timeout_ms;
        uint32_t last_checkin_ms;
    };

    TaskRecord m_records[static_cast<int>(TaskId::MAX_TASKS)];
};

} // namespace rtos
} // namespace rover

#endif // ROVER_WATCHDOG_REGISTRY_H
