/**
 * @file protocol_deserializer.cpp
 * @brief Recon Rover V1 - Protocol Deserializer
 */

#include "protocol_deserializer.h"
#include "packet_validator.h"
#include "json_parser.h"

namespace rover {
namespace comms {

bool ProtocolDeserializer::deserializeCommand(const char* raw_frame, size_t length, CommandPacket& packet) {
    std::string json;
    
    // 1. Validate framing and CRC-16
    if (!PacketValidator::validateAndExtract(raw_frame, length, json)) {
        return false;
    }
    
    // 2. Parse JSON string into CommandPacket
    if (!JsonParser::parseCommand(json, packet)) {
        return false;
    }
    
    return true;
}

} // namespace comms
} // namespace rover
