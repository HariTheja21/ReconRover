/**
 * @file main.cpp
 * @brief Recon Rover V1 - ESP32 Entry Point
 * 
 * Orchestrates boot sequence and FreeRTOS task spawning.
 */

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

#include "configuration_manager.h"
#include "queue_manager.h"
#include "watchdog_registry.h"
#include "task_manager.h"

static const char* TAG = "BOOT";

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "=== Recon Rover V1 ESP32 Boot Sequence ===");

    // 1. Initialize Configuration
    ESP_LOGI(TAG, "Initializing Configuration...");
    rover::ConfigurationManager config;
    // config.init(); // Assuming standard initialization if needed

    // 2. Initialize HAL
    ESP_LOGI(TAG, "Initializing HAL...");
    // HAL initialization is typically handled by drivers or specific HAL modules

    // 3. Initialize Drivers
    ESP_LOGI(TAG, "Initializing Drivers...");
    // Driver initialization deferred to tasks/managers

    // 4. Initialize Managers
    ESP_LOGI(TAG, "Initializing Managers...");
    
    // 5. Initialize QueueManager
    ESP_LOGI(TAG, "Initializing QueueManager...");
    rover::rtos::QueueManager queueManager;
    queueManager.createAllQueues();

    // Watchdog
    ESP_LOGI(TAG, "Initializing Watchdog Registry...");
    rover::rtos::WatchdogRegistry watchdogRegistry;

    // 6. Initialize TaskManager
    ESP_LOGI(TAG, "Initializing TaskManager...");
    rover::rtos::TaskManager taskManager(&queueManager, &watchdogRegistry, &config);

    // 7. Start the Scheduler / Spawn Tasks
    ESP_LOGI(TAG, "Spawning FreeRTOS Tasks...");
    if (taskManager.spawnAllTasks()) {
        ESP_LOGI(TAG, "All tasks spawned successfully.");
    } else {
        ESP_LOGE(TAG, "Failed to spawn one or more tasks! System HALTED.");
        return;
    }

    ESP_LOGI(TAG, "FreeRTOS Scheduler running (managed by ESP-IDF).");
    ESP_LOGI(TAG, "Boot Sequence COMPLETE.");
}

