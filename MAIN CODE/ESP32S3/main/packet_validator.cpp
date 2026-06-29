/**
 * @file packet_validator.cpp
 * @brief Recon Rover V1 - Packet Validator
 */

#include "packet_validator.h"
#include "utils.h"
#include <cstdio>
#include <cstring>

namespace rover {
namespace comms {

bool PacketValidator::validateAndExtract(const char* raw_frame, size_t length, std::string& extracted_json) {
    if (!raw_frame || length < MIN_PACKET_SIZE || length > MAX_PACKET_SIZE) {
        return false;
    }

    if (raw_frame[0] != '^' || raw_frame[length - 1] != '$') {
        return false;
    }

    if (raw_frame[5] != '|') {
        return false;
    }

    // Extract CRC
    char crc_hex[5] = {0};
    std::memcpy(crc_hex, &raw_frame[1], 4);
    uint16_t expected_crc = parseHexCrc(crc_hex);

    // Extract JSON payload
    size_t json_len = length - 7; // ^(1) + CRC(4) + |(1) + $(1) = 7
    std::string json_str(&raw_frame[6], json_len);

    // Verify CRC
    uint16_t computed_crc = utils::crc16(reinterpret_cast<const uint8_t*>(json_str.c_str()), json_len);

    if (computed_crc != expected_crc) {
        return false;
    }

    extracted_json = std::move(json_str);
    return true;
}

std::string PacketValidator::frameAndSign(const std::string& json_payload) {
    uint16_t crc = utils::crc16(reinterpret_cast<const uint8_t*>(json_payload.c_str()), json_payload.length());
    
    std::string frame = "^";
    frame += formatHexCrc(crc);
    frame += "|";
    frame += json_payload;
    frame += "$";
    
    return frame;
}

uint16_t PacketValidator::parseHexCrc(const char* hex_str) {
    uint16_t crc = 0;
    std::sscanf(hex_str, "%04hx", &crc);
    return crc;
}

std::string PacketValidator::formatHexCrc(uint16_t crc) {
    char buf[5];
    std::snprintf(buf, sizeof(buf), "%04X", crc);
    return std::string(buf);
}

} // namespace comms
} // namespace rover
