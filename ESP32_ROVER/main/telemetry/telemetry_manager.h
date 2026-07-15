#pragma once
#include "telemetry_engine.h"
#include "telemetry_health.h"

namespace ReconRover {
namespace Telemetry {

// Simulates the FreeRTOS task manager for Telemetry reporting.
class TelemetryManager {
public:
    TelemetryManager(TelemetryEngine::UartTransmitCallback transmit_cb);

    void Init();
    void Tick(uint32_t current_time_ms);

    TelemetryEngine& GetEngine() { return engine_; }
    TelemetryHealth& GetHealth() { return health_; }

private:
    TelemetryEngine engine_;
    TelemetryHealth health_;
};

} // namespace Telemetry
} // namespace ReconRover
