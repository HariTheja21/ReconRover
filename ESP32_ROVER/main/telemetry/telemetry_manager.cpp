#include "telemetry_manager.h"

namespace ReconRover {
namespace Telemetry {

TelemetryManager::TelemetryManager(TelemetryEngine::UartTransmitCallback transmit_cb)
    : engine_(transmit_cb) {}

void TelemetryManager::Init() {
    // FreeRTOS queue and timer initialization would go here
}

void TelemetryManager::Tick(uint32_t current_time_ms) {
    engine_.Tick(current_time_ms);
    health_.UpdateHealth(current_time_ms);
    
    // In a real system, successful UART transmission triggers RecordPublish()
    health_.RecordPublish(current_time_ms); 
}

} // namespace Telemetry
} // namespace ReconRover
