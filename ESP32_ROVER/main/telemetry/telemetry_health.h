#pragma once
#include <cstdint>

namespace ReconRover {
namespace Telemetry {

class TelemetryHealth {
public:
    TelemetryHealth() : is_healthy_(true), last_publish_ms_(0) {}

    void RecordPublish(uint32_t current_time_ms) {
        last_publish_ms_ = current_time_ms;
        is_healthy_ = true;
    }

    void UpdateHealth(uint32_t current_time_ms) {
        if (current_time_ms - last_publish_ms_ > 2000) {
            is_healthy_ = false;
        }
    }

    bool IsHealthy() const { return is_healthy_; }

private:
    bool is_healthy_;
    uint32_t last_publish_ms_;
};

} // namespace Telemetry
} // namespace ReconRover
