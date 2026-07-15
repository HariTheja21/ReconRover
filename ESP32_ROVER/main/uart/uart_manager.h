#pragma once
#include "uart_engine.h"

namespace ReconRover {
namespace UART {

class UartManager {
public:
    UartManager(UartEngine::PacketReceivedCallback rx_cb, UartEngine::HardwareTxCallback tx_cb);

    void Init();
    
    // Polled from RTOS task
    void Tick(uint32_t current_time_ms);
    
    // Inject bytes coming from the ESP-IDF UART ISR
    void OnIsrByteReceived(uint8_t byte);

    // Provide packets from the Telemetry Engine
    void EnqueueTelemetryPacket(const UartPacket& packet);

    UartEngine& GetEngine() { return engine_; }

private:
    UartEngine engine_;
};

} // namespace UART
} // namespace ReconRover
