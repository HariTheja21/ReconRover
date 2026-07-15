#pragma once
#include <cstdint>

namespace ReconRover {
namespace UART {

class UartHealth {
public:
    UartHealth() : is_healthy_(true), last_rx_ms_(0), last_tx_ms_(0) {}

    void RecordRx(uint32_t current_time_ms) {
        last_rx_ms_ = current_time_ms;
        is_healthy_ = true;
    }

    void RecordTx(uint32_t current_time_ms) {
        last_tx_ms_ = current_time_ms;
    }

    void RecordError() {
        is_healthy_ = false;
    }

    bool IsHealthy() const { return is_healthy_; }

private:
    bool is_healthy_;
    uint32_t last_rx_ms_;
    uint32_t last_tx_ms_;
};

} // namespace UART
} // namespace ReconRover
