#include "telemetry_engine.h"

namespace ReconRover {
namespace Telemetry {

TelemetryEngine::TelemetryEngine(UartTransmitCallback transmit_cb)
    : stats_(), scheduler_(), encoder_(stats_), builder_(encoder_, stats_), transmit_cb_(transmit_cb) {}

void TelemetryEngine::Tick(uint32_t current_time_ms) {
    scheduler_.Tick(current_time_ms);

    if (scheduler_.ShouldSendHeartbeat()) {
        GatherAndSendHeartbeat(current_time_ms);
    }
    
    if (scheduler_.ShouldSendMotorStatus()) {
        GatherAndSendMotorStatus(current_time_ms);
    }

    scheduler_.ClearFlags();
}

void TelemetryEngine::GatherAndSendHeartbeat(uint32_t time_ms) {
    TelemetryEvent event;
    event.type = TelemetryType::HEARTBEAT;
    event.timestamp_ms = time_ms;
    event.payload.heartbeat.uptime_s = time_ms / 1000;

    TelemetryPacket packet;
    builder_.Build(event, packet);

    if (transmit_cb_) {
        transmit_cb_(packet.buffer, packet.length);
    }
    stats_.heartbeats_sent++;
}

void TelemetryEngine::GatherAndSendMotorStatus(uint32_t time_ms) {
    TelemetryEvent event;
    event.type = TelemetryType::MOTOR_STATUS;
    event.timestamp_ms = time_ms;
    // Real implementation would pull this from Driver layer or global state
    event.payload.motor.left_v = 0; 
    event.payload.motor.right_v = 0; 

    TelemetryPacket packet;
    builder_.Build(event, packet);

    if (transmit_cb_) {
        transmit_cb_(packet.buffer, packet.length);
    }
}

} // namespace Telemetry
} // namespace ReconRover
