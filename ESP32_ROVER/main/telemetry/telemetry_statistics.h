#pragma once
#include <cstdint>

namespace ReconRover {
namespace Telemetry {

struct TelemetryStatistics {
    uint32_t packets_generated = 0;
    uint32_t bytes_encoded = 0;
    uint32_t heartbeats_sent = 0;
    uint32_t skipped_cycles = 0;
};

} // namespace Telemetry
} // namespace ReconRover
