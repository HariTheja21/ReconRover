#pragma once
#include <cstdint>

namespace ReconRover {
namespace Telemetry {

class TelemetryScheduler {
public:
    TelemetryScheduler();

    void Tick(uint32_t current_time_ms);
    
    bool ShouldSendHeartbeat() const { return send_heartbeat_; }
    bool ShouldSendMotorStatus() const { return send_motor_; }
    
    void ClearFlags();

private:
    uint32_t last_heartbeat_ms_;
    uint32_t last_motor_ms_;
    
    bool send_heartbeat_;
    bool send_motor_;
};

} // namespace Telemetry
} // namespace ReconRover
