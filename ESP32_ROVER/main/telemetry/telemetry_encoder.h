#pragma once
#include "telemetry_events.h"
#include "telemetry_statistics.h"

namespace ReconRover {
namespace Telemetry {

class TelemetryEncoder {
public:
    TelemetryEncoder(TelemetryStatistics& stats);

    // Formats the abstract event into raw payload bytes depending on type
    void EncodePayload(const TelemetryEvent& event, uint8_t* payload_buffer, uint8_t& payload_length);

private:
    TelemetryStatistics& stats_;
};

} // namespace Telemetry
} // namespace ReconRover
