/**
 * @file command_router.h
 * @brief Recon Rover V1 - Command Router
 *
 * Translates a decoded CommandPacket into discrete CommandEvents
 * and pushes them to the appropriate subsystem queues.
 */

#ifndef ROVER_COMMAND_ROUTER_H
#define ROVER_COMMAND_ROUTER_H

#include "types_protocol.h"
#include "messages.h"
#include "queue_manager.h"

namespace rover {
namespace comms {

/**
 * @class CommandRouter
 * @brief Routes commands to freeRTOS queues.
 */
class CommandRouter {
public:
    /**
     * @brief Constructor.
     * @param queue Pointer to the global QueueManager.
     */
    explicit CommandRouter(rtos::QueueManager* queue);

    /**
     * @brief Routes the packet to the necessary queues.
     * @param packet The decoded command packet.
     */
    void route(const CommandPacket& packet);

private:
    rtos::QueueManager* m_queue;
};

} // namespace comms
} // namespace rover

#endif // ROVER_COMMAND_ROUTER_H
