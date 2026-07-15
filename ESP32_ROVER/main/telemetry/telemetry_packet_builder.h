#pragma once
#include "telemetry_events.h"
#include "telemetry_encoder.h"
#include "telemetry_statistics.h"

namespace ReconRover {
namespace Telemetry {

class TelemetryPacketBuilder {
public:
    static constexpr uint8_t HEADER_1 = 0xAA;
    static constexpr uint8_t HEADER_2 = 0x55;

    TelemetryPacketBuilder(TelemetryEncoder& encoder, TelemetryStatistics& stats);

    void Build(const TelemetryEvent& event, TelemetryPacket& out_packet);

private:
    TelemetryEncoder& encoder_;
    TelemetryStatistics& stats_;
    uint8_t next_sequence_;

    uint8_t CalculateCRC(const uint8_t* data, uint8_t length);
};

} // namespace Telemetry
} // namespace ReconRover
