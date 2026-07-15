#include "packet_validator.h"

namespace ReconRover {
namespace Runtime {

PacketValidator::PacketValidator(RuntimeStatistics& stats) 
    : stats_(stats), last_sequence_(0), first_packet_(true) {}

uint8_t PacketValidator::CalculateCRC(const uint8_t* data, size_t length) {
    uint8_t crc = 0;
    for (size_t i = 0; i < length; ++i) {
        crc ^= data[i];
    }
    return crc;
}

bool PacketValidator::Validate(const uint8_t* packet, size_t length) {
    if (length != PACKET_LENGTH) return false;

    if (packet[0] != HEADER_1 || packet[1] != HEADER_2) {
        stats_.packets_invalid_header++;
        return false;
    }

    uint8_t provided_crc = packet[PACKET_LENGTH - 1];
    uint8_t calculated_crc = CalculateCRC(packet, PACKET_LENGTH - 1);

    if (provided_crc != calculated_crc) {
        stats_.packets_invalid_crc++;
        return false;
    }

    uint8_t sequence = packet[3];
    if (!first_packet_) {
        // Detect exact duplicate
        if (sequence == last_sequence_) {
            stats_.packets_dropped_duplicate++;
            return false; // Silently drop exact duplicates
        }
    }

    first_packet_ = false;
    last_sequence_ = sequence;
    stats_.packets_valid++;
    return true;
}

} // namespace Runtime
} // namespace ReconRover
