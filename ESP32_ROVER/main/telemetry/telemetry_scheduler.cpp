#include "telemetry_scheduler.h"

namespace ReconRover {
namespace Telemetry {

TelemetryScheduler::TelemetryScheduler()
    : last_heartbeat_ms_(0), last_motor_ms_(0),
      send_heartbeat_(false), send_motor_(false) {}

void TelemetryScheduler::Tick(uint32_t current_time_ms) {
    // 1 Hz Heartbeat
    if (current_time_ms - last_heartbeat_ms_ >= 1000) {
        send_heartbeat_ = true;
        last_heartbeat_ms_ = current_time_ms;
    }
    
    // 10 Hz Motor Status
    if (current_time_ms - last_motor_ms_ >= 100) {
        send_motor_ = true;
        last_motor_ms_ = current_time_ms;
    }
}

void TelemetryScheduler::ClearFlags() {
    send_heartbeat_ = false;
    send_motor_ = false;
}

} // namespace Telemetry
} // namespace ReconRover
