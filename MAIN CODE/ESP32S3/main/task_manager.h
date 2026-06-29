/**
 * @file task_manager.h
 * @brief Recon Rover V1 - RTOS Task Manager
 *
 * Orchestrates the creation, startup, and shutdown order of FreeRTOS tasks.
 */

#ifndef ROVER_TASK_MANAGER_H
#define ROVER_TASK_MANAGER_H

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "queue_manager.h"
#include "watchdog_registry.h"
#include "configuration_manager.h"

namespace rover {
namespace rtos {

/**
 * @struct TaskContext
 * @brief Passed as pvParameters to all tasks to inject infrastructure dependencies.
 */
struct TaskContext {
    QueueManager* queue;
    WatchdogRegistry* watchdog;
    ConfigurationManager* config;
};

/**
 * @class TaskManager
 * @brief Encapsulates RTOS task creation and lifecycle management.
 */
class TaskManager {
public:
    /**
     * @brief Constructs the TaskManager with needed OS dependencies.
     */
    TaskManager(QueueManager* q, WatchdogRegistry* w, ConfigurationManager* c);
    ~TaskManager();

    /**
     * @brief Creates and starts all background tasks in the correct priority and core order.
     * @return True if all tasks successfully created.
     */
    bool spawnAllTasks();

    /**
     * @brief Initiates a graceful shutdown of all tasks.
     */
    void shutdownAllTasks();

private:
    QueueManager* m_queue;
    WatchdogRegistry* m_watchdog;
    ConfigurationManager* m_config;
    TaskContext m_ctx;

    TaskHandle_t t_watchdog;
    TaskHandle_t t_serial;
    TaskHandle_t t_motor;
    TaskHandle_t t_sensor;
    TaskHandle_t t_servo;
    TaskHandle_t t_oled;
    TaskHandle_t t_led;
    TaskHandle_t t_telemetry;
    TaskHandle_t t_health;
    TaskHandle_t t_fault;

    // These are static stubs. The actual implementations will be provided
    // in Phase 2.3D where task bodies are written.
    static void watchdogTask(void* pvParameters);
    static void serialTask(void* pvParameters);
    static void motorTask(void* pvParameters);
    static void sensorTask(void* pvParameters);
    static void servoTask(void* pvParameters);
    static void oledTask(void* pvParameters);
    static void ledTask(void* pvParameters);
    static void telemetryTask(void* pvParameters);
    static void healthTask(void* pvParameters);
    static void faultTask(void* pvParameters);
};

} // namespace rtos
} // namespace rover

#endif // ROVER_TASK_MANAGER_H
