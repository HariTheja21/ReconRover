/**
 * @file telemetry_router.h
 * @brief Recon Rover V1 - Telemetry Router
 *
 * Aggregates Queue events into a TelemetryPacket for serialization.
 */

#ifndef ROVER_TELEMETRY_ROUTER_H
#define ROVER_TELEMETRY_ROUTER_H

#include "types_protocol.h"
#include "messages.h"
#include "queue_manager.h"

namespace rover {
namespace comms {

/**
 * @class TelemetryRouter
 * @brief Builds the outgoing telemetry packet.
 */
class TelemetryRouter {
public:
    /**
     * @brief Processes an incoming SensorEvent and updates the cached packet.
     * @param event The new sensor data.
     */
    void processSensorEvent(const SensorEvent& event);

    /**
     * @brief Processes an incoming HealthEvent and updates the cached packet.
     * @param health The new health data.
     */
    void processHealthEvent(const SystemHealth& health);

    /**
     * @brief Retrieves the latest aggregated telemetry packet.
     * @return The populated telemetry packet.
     */
    const TelemetryPacket& getPacket() const;

private:
    TelemetryPacket m_packet = {};
};

} // namespace comms
} // namespace rover

#endif // ROVER_TELEMETRY_ROUTER_H
