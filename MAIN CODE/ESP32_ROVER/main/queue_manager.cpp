/**
 * @file queue_manager.cpp
 * @brief Recon Rover V1 - RTOS Queue Manager
 */

#include "queue_manager.h"
#include "rtos_config.h"

namespace rover {
namespace rtos {

QueueManager::QueueManager()
    : q_sensor(nullptr), q_telemetry(nullptr), q_command(nullptr),
      q_motor(nullptr), q_servo(nullptr), q_oled(nullptr), q_led(nullptr),
      q_health(nullptr), q_fault(nullptr), q_system(nullptr) {
}

QueueManager::~QueueManager() {
    if (q_sensor) vQueueDelete(q_sensor);
    if (q_telemetry) vQueueDelete(q_telemetry);
    if (q_command) vQueueDelete(q_command);
    if (q_motor) vQueueDelete(q_motor);
    if (q_servo) vQueueDelete(q_servo);
    if (q_oled) vQueueDelete(q_oled);
    if (q_led) vQueueDelete(q_led);
    if (q_health) vQueueDelete(q_health);
    if (q_fault) vQueueDelete(q_fault);
    if (q_system) vQueueDelete(q_system);
}

bool QueueManager::init() {
    q_sensor    = xQueueCreate(Q_LEN_SENSOR,    sizeof(SensorEvent));
    q_telemetry = xQueueCreate(Q_LEN_TELEMETRY, sizeof(TelemetryPacket));
    q_command   = xQueueCreate(Q_LEN_COMMAND,   sizeof(CommandEvent));
    q_motor     = xQueueCreate(Q_LEN_MOTOR,     sizeof(CommandEvent));
    q_servo     = xQueueCreate(Q_LEN_SERVO,     sizeof(CommandEvent));
    q_oled      = xQueueCreate(Q_LEN_OLED,      sizeof(CommandEvent));
    q_led       = xQueueCreate(Q_LEN_LED,       sizeof(CommandEvent));
    q_health    = xQueueCreate(Q_LEN_HEALTH,    sizeof(SystemHealth));
    q_fault     = xQueueCreate(Q_LEN_FAULT,     sizeof(FaultEvent));
    q_system    = xQueueCreate(Q_LEN_SYSTEM,    sizeof(SystemEvent));

    return (q_sensor && q_telemetry && q_command && q_motor && 
            q_servo && q_oled && q_led && q_health && q_fault && q_system);
}

// =========================================================================
// Helper Macro for standard queue wrappers
// =========================================================================
#define SEND_TO_QUEUE(handle, item, wait) \
    if (!handle) return false; \
    return (xQueueSend(handle, &(item), (wait == portMAX_DELAY ? portMAX_DELAY : pdMS_TO_TICKS(wait))) == pdTRUE)

#define RECV_FROM_QUEUE(handle, item, wait) \
    if (!handle) return false; \
    return (xQueueReceive(handle, &(item), (wait == portMAX_DELAY ? portMAX_DELAY : pdMS_TO_TICKS(wait))) == pdTRUE)

// =========================================================================
// Send APIs
// =========================================================================
bool QueueManager::sendSensorEvent(const SensorEvent& event, uint32_t wait_ms)       { SEND_TO_QUEUE(q_sensor, event, wait_ms); }
bool QueueManager::sendTelemetryEvent(const TelemetryPacket& packet, uint32_t wait_ms) { SEND_TO_QUEUE(q_telemetry, packet, wait_ms); }
bool QueueManager::sendCommandEvent(const CommandEvent& event, uint32_t wait_ms)     { SEND_TO_QUEUE(q_command, event, wait_ms); }
bool QueueManager::sendMotorEvent(const CommandEvent& event, uint32_t wait_ms)       { SEND_TO_QUEUE(q_motor, event, wait_ms); }
bool QueueManager::sendServoEvent(const CommandEvent& event, uint32_t wait_ms)       { SEND_TO_QUEUE(q_servo, event, wait_ms); }
bool QueueManager::sendOledEvent(const CommandEvent& event, uint32_t wait_ms)        { SEND_TO_QUEUE(q_oled, event, wait_ms); }
bool QueueManager::sendLedEvent(const CommandEvent& event, uint32_t wait_ms)         { SEND_TO_QUEUE(q_led, event, wait_ms); }
bool QueueManager::sendHealthEvent(const SystemHealth& health, uint32_t wait_ms)     { SEND_TO_QUEUE(q_health, health, wait_ms); }
bool QueueManager::sendFaultEvent(const FaultEvent& event, uint32_t wait_ms)         { SEND_TO_QUEUE(q_fault, event, wait_ms); }
bool QueueManager::sendSystemEvent(const SystemEvent& event, uint32_t wait_ms)       { SEND_TO_QUEUE(q_system, event, wait_ms); }

// =========================================================================
// Receive APIs
// =========================================================================
bool QueueManager::receiveSensorEvent(SensorEvent& event, uint32_t wait_ms)          { RECV_FROM_QUEUE(q_sensor, event, wait_ms); }
bool QueueManager::receiveTelemetryEvent(TelemetryPacket& packet, uint32_t wait_ms)  { RECV_FROM_QUEUE(q_telemetry, packet, wait_ms); }
bool QueueManager::receiveCommandEvent(CommandEvent& event, uint32_t wait_ms)        { RECV_FROM_QUEUE(q_command, event, wait_ms); }
bool QueueManager::receiveMotorEvent(CommandEvent& event, uint32_t wait_ms)          { RECV_FROM_QUEUE(q_motor, event, wait_ms); }
bool QueueManager::receiveServoEvent(CommandEvent& event, uint32_t wait_ms)          { RECV_FROM_QUEUE(q_servo, event, wait_ms); }
bool QueueManager::receiveOledEvent(CommandEvent& event, uint32_t wait_ms)           { RECV_FROM_QUEUE(q_oled, event, wait_ms); }
bool QueueManager::receiveLedEvent(CommandEvent& event, uint32_t wait_ms)            { RECV_FROM_QUEUE(q_led, event, wait_ms); }
bool QueueManager::receiveHealthEvent(SystemHealth& health, uint32_t wait_ms)        { RECV_FROM_QUEUE(q_health, health, wait_ms); }
bool QueueManager::receiveFaultEvent(FaultEvent& event, uint32_t wait_ms)            { RECV_FROM_QUEUE(q_fault, event, wait_ms); }
bool QueueManager::receiveSystemEvent(SystemEvent& event, uint32_t wait_ms)          { RECV_FROM_QUEUE(q_system, event, wait_ms); }

} // namespace rtos
} // namespace rover
