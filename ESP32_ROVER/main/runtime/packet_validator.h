#pragma once
#include <cstdint>
#include <cstddef>
#include "runtime_statistics.h"

namespace ReconRover {
namespace Runtime {

class PacketValidator {
public:
    static constexpr uint8_t HEADER_1 = 0xAA;
    static constexpr uint8_t HEADER_2 = 0x55;
    static constexpr size_t PACKET_LENGTH = 9;

    PacketValidator(RuntimeStatistics& stats);

    bool Validate(const uint8_t* packet, size_t length);
    static uint8_t CalculateCRC(const uint8_t* data, size_t length);

private:
    RuntimeStatistics& stats_;
    uint8_t last_sequence_;
    bool first_packet_;
};

} // namespace Runtime
} // namespace ReconRover
