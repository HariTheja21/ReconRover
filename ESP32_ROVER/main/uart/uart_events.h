#pragma once
#include <cstdint>

namespace ReconRover {
namespace UART {

// Abstraction for a generic packet (used for both RX and TX)
struct UartPacket {
    static constexpr uint8_t MAX_LENGTH = 16;
    uint8_t buffer[MAX_LENGTH];
    uint8_t length;
};

} // namespace UART
} // namespace ReconRover
