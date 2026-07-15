#pragma once
#include "telemetry_events.h"
#include "telemetry_scheduler.h"
#include "telemetry_encoder.h"
#include "telemetry_packet_builder.h"
#include "telemetry_statistics.h"

namespace ReconRover {
namespace Telemetry {

class TelemetryEngine {
public:
    // Requires a callback or interface to inject into UART Tx queue.
    // Abstracting it via a function pointer for zero dynamic allocation coupling.
    using UartTransmitCallback = void(*)(const uint8_t* data, uint8_t length);

    TelemetryEngine(UartTransmitCallback transmit_cb);

    void Tick(uint32_t current_time_ms);

    TelemetryStatistics& GetStatistics() { return stats_; }

private:
    TelemetryStatistics stats_;
    TelemetryScheduler scheduler_;
    TelemetryEncoder encoder_;
    TelemetryPacketBuilder builder_;
    UartTransmitCallback transmit_cb_;

    void GatherAndSendHeartbeat(uint32_t time_ms);
    void GatherAndSendMotorStatus(uint32_t time_ms);
};

} // namespace Telemetry
} // namespace ReconRover
