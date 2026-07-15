#include "uart_manager.h"

namespace ReconRover {
namespace UART {

UartManager::UartManager(UartEngine::PacketReceivedCallback rx_cb, UartEngine::HardwareTxCallback tx_cb)
    : engine_(rx_cb, tx_cb) {}

void UartManager::Init() {
    // ESP-IDF UART driver initialization:
    // uart_config_t uart_config = {...}
    // uart_param_config(UART_NUM_1, &uart_config);
    // uart_set_pin(UART_NUM_1, TXD, RXD, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    // uart_driver_install(UART_NUM_1, RX_BUF_SIZE * 2, TX_BUF_SIZE * 2, 20, &uart_queue, 0);
}

void UartManager::Tick(uint32_t current_time_ms) {
    // Attempt to flush buffered TX bytes out to hardware driver
    engine_.TickTx();
}

void UartManager::OnIsrByteReceived(uint8_t byte) {
    // This feeds the internal framer state machine
    engine_.ProcessRxByte(byte);
}

void UartManager::EnqueueTelemetryPacket(const UartPacket& packet) {
    engine_.QueueTxPacket(packet);
}

} // namespace UART
} // namespace ReconRover
