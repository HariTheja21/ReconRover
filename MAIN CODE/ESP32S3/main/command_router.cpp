/**
 * @file command_router.cpp
 * @brief Recon Rover V1 - Command Router
 */

#include "command_router.h"

namespace rover {
namespace comms {

CommandRouter::CommandRouter(rtos::QueueManager* queue) : m_queue(queue) {}

void CommandRouter::route(const CommandPacket& packet) {
    if (!m_queue) return;

    if (packet.has_motor_cmd) {
        CommandEvent evt = {};
        evt.type = EventType::CMD_MOTOR;
        evt.data.motor = packet.motor_cmd;
        m_queue->sendMotorEvent(evt, 0); // Non-blocking
    }

    if (packet.has_servo_cmd) {
        CommandEvent evt = {};
        evt.type = EventType::CMD_SERVO;
        evt.data.servo = packet.servo_cmd;
        m_queue->sendServoEvent(evt, 0);
    }

    if (packet.has_eye_cmd) {
        CommandEvent evt = {};
        evt.type = EventType::CMD_EYE;
        evt.data.eye = packet.eye_cmd;
        m_queue->sendOledEvent(evt, 0);
    }

    if (packet.has_led_cmd) {
        CommandEvent evt = {};
        evt.type = EventType::CMD_LED;
        evt.data.led = packet.led_cmd;
        m_queue->sendLedEvent(evt, 0);
    }
}

} // namespace comms
} // namespace rover
