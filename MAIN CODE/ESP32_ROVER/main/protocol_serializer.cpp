/**
 * @file protocol_serializer.cpp
 * @brief Recon Rover V1 - Protocol Serializer
 */

#include "protocol_serializer.h"
#include "json_builder.h"
#include "packet_validator.h"

namespace rover {
namespace comms {

std::string ProtocolSerializer::serializeTelemetry(const TelemetryPacket& packet) {
    std::string json = JsonBuilder::buildTelemetry(packet);
    return PacketValidator::frameAndSign(json);
}

std::string ProtocolSerializer::serializeHealth(const SystemHealth& health) {
    std::string json = JsonBuilder::buildHealth(health);
    return PacketValidator::frameAndSign(json);
}

std::string ProtocolSerializer::serializeFault(const Error& fault) {
    std::string json = JsonBuilder::buildFault(fault);
    return PacketValidator::frameAndSign(json);
}

} // namespace comms
} // namespace rover
