#pragma once
#include "uart_receiver.h"
#include "uart_transmitter.h"
#include "uart_statistics.h"
#include "uart_health.h"

namespace ReconRover {
namespace UART {

class UartEngine {
public:
    // Callbacks to bridge upward to Runtime (RX) and downward to HW Driver
    using PacketReceivedCallback = void(*)(const UartPacket& packet);
    using HardwareTxCallback = void(*)(uint8_t byte);

    UartEngine(PacketReceivedCallback rx_cb, HardwareTxCallback tx_cb);

    // Call this when hardware receives a byte
    void ProcessRxByte(uint8_t byte);

    // Call this when Telemetry layer wants to send a packet
    void QueueTxPacket(const UartPacket& packet);

    // Call this in the main loop to process outgoing bytes
    void TickTx();

    UartStatistics& GetStatistics() { return stats_; }
    UartHealth& GetHealth() { return health_; }

private:
    UartStatistics stats_;
    UartHealth health_;
    UartReceiver receiver_;
    UartTransmitter transmitter_;

    PacketReceivedCallback rx_cb_;
    HardwareTxCallback tx_cb_;
};

} // namespace UART
} // namespace ReconRover
