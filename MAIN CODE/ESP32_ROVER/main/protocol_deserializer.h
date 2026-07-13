/**
 * @file protocol_deserializer.h
 * @brief Recon Rover V1 - Protocol Deserializer
 *
 * Coordinates frame validation, CRC checking, and JSON parsing.
 */

#ifndef ROVER_PROTOCOL_DESERIALIZER_H
#define ROVER_PROTOCOL_DESERIALIZER_H

#include "types_protocol.h"
#include <string>

namespace rover {
namespace comms {

/**
 * @class ProtocolDeserializer
 * @brief Coordinates validation and deserialization.
 */
class ProtocolDeserializer {
public:
    /**
     * @brief Validates a raw string frame and parses it into a CommandPacket.
     * @param raw_frame The raw string including framing characters.
     * @param length The length of the raw string.
     * @param[out] packet The parsed output.
     * @return True if validation and parsing were fully successful.
     */
    static bool deserializeCommand(const char* raw_frame, size_t length, CommandPacket& packet);
};

} // namespace comms
} // namespace rover

#endif // ROVER_PROTOCOL_DESERIALIZER_H
