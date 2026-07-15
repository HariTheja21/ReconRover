#pragma once
#include <cstdint>
#include "runtime_statistics.h"

namespace ReconRover {
namespace Runtime {

class RuntimeHealth {
public:
    RuntimeHealth() : is_healthy(true), last_packet_time_ms(0) {}

    void UpdateHealth(uint32_t current_time_ms) {
        // Example logic: if no packet for 1000ms, mark unhealthy (timeout)
        if (current_time_ms - last_packet_time_ms > 1000) {
            is_healthy = false;
        } else {
            is_healthy = true;
        }
    }

    void RecordPacketArrival(uint32_t current_time_ms) {
        last_packet_time_ms = current_time_ms;
        is_healthy = true;
    }

    bool IsHealthy() const { return is_healthy; }

private:
    bool is_healthy;
    uint32_t last_packet_time_ms;
};

} // namespace Runtime
} // namespace ReconRover
