/**
 * @file protocol_serializer.h
 * @brief Recon Rover V1 - Protocol Serializer
 *
 * High-level wrapper that constructs JSON and signs/frames it for transmission.
 */

#ifndef ROVER_PROTOCOL_SERIALIZER_H
#define ROVER_PROTOCOL_SERIALIZER_H

#include "types_protocol.h"
#include "health_system.h"
#include "error_system.h"
#include <string>

namespace rover {
namespace comms {

/**
 * @class ProtocolSerializer
 * @brief Coordinates JSON generation and CRC framing.
 */
class ProtocolSerializer {
public:
    static std::string serializeTelemetry(const TelemetryPacket& packet);
    static std::string serializeHealth(const SystemHealth& health);
    static std::string serializeFault(const Error& fault);
};

} // namespace comms
} // namespace rover

#endif // ROVER_PROTOCOL_SERIALIZER_H
