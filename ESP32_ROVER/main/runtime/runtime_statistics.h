#pragma once
#include <cstdint>

namespace ReconRover {
namespace Runtime {

struct RuntimeStatistics {
    uint32_t packets_received = 0;
    uint32_t packets_valid = 0;
    uint32_t packets_invalid_header = 0;
    uint32_t packets_invalid_crc = 0;
    uint32_t packets_dropped_duplicate = 0;
    uint32_t bytes_processed = 0;
    uint32_t events_dispatched = 0;
};

} // namespace Runtime
} // namespace ReconRover
