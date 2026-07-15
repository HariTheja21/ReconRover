#include "uart_engine.h"

namespace ReconRover {
namespace UART {

UartEngine::UartEngine(PacketReceivedCallback rx_cb, HardwareTxCallback tx_cb)
    : stats_(), health_(), receiver_(stats_), transmitter_(stats_),
      rx_cb_(rx_cb), tx_cb_(tx_cb) {}

void UartEngine::ProcessRxByte(uint8_t byte) {
    receiver_.ProcessByte(byte);
    if (receiver_.HasPacket()) {
        UartPacket packet;
        if (receiver_.GetPacket(packet) && rx_cb_) {
            rx_cb_(packet);
            // Time injection deferred to Manager layer in real app, mock it here
            health_.RecordRx(0); 
        }
    }
}

void UartEngine::QueueTxPacket(const UartPacket& packet) {
    if (!transmitter_.QueuePacket(packet)) {
        health_.RecordError();
    }
}

void UartEngine::TickTx() {
    uint8_t byte;
    // Process a max of 16 bytes per tick to avoid blocking RTOS
    for (int i = 0; i < 16; i++) {
        if (transmitter_.GetNextByte(byte)) {
            if (tx_cb_) {
                tx_cb_(byte);
                health_.RecordTx(0);
            }
        } else {
            break; // Queue empty
        }
    }
}

} // namespace UART
} // namespace ReconRover
