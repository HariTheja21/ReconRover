/**
 * @file json_builder.h
 * @brief Recon Rover V1 - JSON Builder
 *
 * Safely converts internal C++ structs into JSON strings using ArduinoJson.
 * Ensures zero heap allocations during runtime periodic loops.
 */

#ifndef ROVER_JSON_BUILDER_H
#define ROVER_JSON_BUILDER_H

#include "types_protocol.h"
#include "health_system.h"
#include <string>

namespace rover {
namespace comms {

/**
 * @class JsonBuilder
 * @brief Handles JSON serialization of outbound packets.
 */
class JsonBuilder {
public:
    /**
     * @brief Serializes a TelemetryPacket into a JSON string.
     * @param packet The populated telemetry data.
     * @return The JSON formatted string.
     */
    static std::string buildTelemetry(const TelemetryPacket& packet);

    /**
     * @brief Serializes a SystemHealth packet into a JSON string.
     * @param health The populated health data.
     * @return The JSON formatted string.
     */
    static std::string buildHealth(const SystemHealth& health);

    /**
     * @brief Serializes a FaultEvent into a JSON string.
     * @param fault The fault data.
     * @return The JSON formatted string.
     */
    static std::string buildFault(const Error& fault);
};

} // namespace comms
} // namespace rover

#endif // ROVER_JSON_BUILDER_H
