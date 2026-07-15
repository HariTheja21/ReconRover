#pragma once
#include <cstdint>

namespace ReconRover {
namespace UART {

struct UartStatistics {
    uint32_t bytes_received = 0;
    uint32_t bytes_transmitted = 0;
    uint32_t packets_received = 0;
    uint32_t packets_transmitted = 0;
    uint32_t buffer_overflows = 0;
    uint32_t framing_errors = 0;
};

} // namespace UART
} // namespace ReconRover
