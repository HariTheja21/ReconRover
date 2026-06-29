/**
 * @file queue_manager.h
 * @brief Recon Rover V1 - RTOS Queue Manager
 *
 * Centralized registry and ownership of all FreeRTOS queues used
 * for inter-process communication between subsystems.
 */

#ifndef ROVER_QUEUE_MANAGER_H
#define ROVER_QUEUE_MANAGER_H

#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "messages.h"

namespace rover {
namespace rtos {

/**
 * @class QueueManager
 * @brief Encapsulates FreeRTOS queue creation and typed access APIs.
 */
class QueueManager {
public:
    QueueManager();
    ~QueueManager();

    /**
     * @brief Creates all system queues according to defined sizes.
     * @return True if all queues were created successfully.
     */
    bool init();

    // =========================================================================
    // Send APIs
    // =========================================================================
    bool sendSensorEvent(const SensorEvent& event, uint32_t wait_ms = 0);
    bool sendTelemetryEvent(const TelemetryPacket& packet, uint32_t wait_ms = 0);
    bool sendCommandEvent(const CommandEvent& event, uint32_t wait_ms = 0);
    bool sendMotorEvent(const CommandEvent& event, uint32_t wait_ms = 0);
    bool sendServoEvent(const CommandEvent& event, uint32_t wait_ms = 0);
    bool sendOledEvent(const CommandEvent& event, uint32_t wait_ms = 0);
    bool sendLedEvent(const CommandEvent& event, uint32_t wait_ms = 0);
    bool sendHealthEvent(const SystemHealth& health, uint32_t wait_ms = 0);
    bool sendFaultEvent(const FaultEvent& event, uint32_t wait_ms = 0);
    bool sendSystemEvent(const SystemEvent& event, uint32_t wait_ms = portMAX_DELAY);

    // =========================================================================
    // Receive APIs
    // =========================================================================
    bool receiveSensorEvent(SensorEvent& event, uint32_t wait_ms = portMAX_DELAY);
    bool receiveTelemetryEvent(TelemetryPacket& packet, uint32_t wait_ms = portMAX_DELAY);
    bool receiveCommandEvent(CommandEvent& event, uint32_t wait_ms = portMAX_DELAY);
    bool receiveMotorEvent(CommandEvent& event, uint32_t wait_ms = portMAX_DELAY);
    bool receiveServoEvent(CommandEvent& event, uint32_t wait_ms = portMAX_DELAY);
    bool receiveOledEvent(CommandEvent& event, uint32_t wait_ms = portMAX_DELAY);
    bool receiveLedEvent(CommandEvent& event, uint32_t wait_ms = portMAX_DELAY);
    bool receiveHealthEvent(SystemHealth& health, uint32_t wait_ms = portMAX_DELAY);
    bool receiveFaultEvent(FaultEvent& event, uint32_t wait_ms = portMAX_DELAY);
    bool receiveSystemEvent(SystemEvent& event, uint32_t wait_ms = portMAX_DELAY);

private:
    QueueHandle_t q_sensor;
    QueueHandle_t q_telemetry;
    QueueHandle_t q_command;
    QueueHandle_t q_motor;
    QueueHandle_t q_servo;
    QueueHandle_t q_oled;
    QueueHandle_t q_led;
    QueueHandle_t q_health;
    QueueHandle_t q_fault;
    QueueHandle_t q_system;
};

} // namespace rtos
} // namespace rover

#endif // ROVER_QUEUE_MANAGER_H
