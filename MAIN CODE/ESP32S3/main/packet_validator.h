/**
 * @file packet_validator.h
 * @brief Recon Rover V1 - Packet Validator
 *
 * Validates framed serial packets, checks lengths, and verifies CRC-16
 * before handing off to the JSON parser.
 *
 * Frame Format: ^[CRC16_HEX]|[JSON_PAYLOAD]$
 * Example: ^A1B2|{"cmd": ...}$
 */

#ifndef ROVER_PACKET_VALIDATOR_H
#define ROVER_PACKET_VALIDATOR_H

#include <cstdint>
#include <cstddef>
#include <string>

namespace rover {
namespace comms {

/**
 * @class PacketValidator
 * @brief Validates and extracts JSON from framed packets.
 */
class PacketValidator {
public:
    static constexpr size_t MAX_PACKET_SIZE = 1024;
    static constexpr size_t MIN_PACKET_SIZE = 8; // ^0000|{}$

    /**
     * @brief Checks frame markers and CRC.
     * @param raw_frame The incoming raw buffer.
     * @param length The length of the raw buffer.
     * @param[out] extracted_json The JSON payload if valid.
     * @return True if the packet is perfectly valid.
     */
    static bool validateAndExtract(const char* raw_frame, size_t length, std::string& extracted_json);

    /**
     * @brief Wraps a JSON payload into a valid framed packet with CRC.
     * @param json_payload The raw JSON string.
     * @return The framed packet ready for transmission.
     */
    static std::string frameAndSign(const std::string& json_payload);

private:
    static uint16_t parseHexCrc(const char* hex_str);
    static std::string formatHexCrc(uint16_t crc);
};

} // namespace comms
} // namespace rover

#endif // ROVER_PACKET_VALIDATOR_H
