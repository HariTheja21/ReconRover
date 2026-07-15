#include "uart_transmitter.h"

namespace ReconRover {
namespace UART {

UartTransmitter::UartTransmitter(UartStatistics& stats) : stats_(stats) {}

bool UartTransmitter::QueuePacket(const UartPacket& packet) {
    if (tx_buffer_.Count() + packet.length > 256) {
        stats_.buffer_overflows++;
        return false;
    }

    for (uint8_t i = 0; i < packet.length; i++) {
        tx_buffer_.Push(packet.buffer[i]);
    }
    
    stats_.packets_transmitted++;
    return true;
}

bool UartTransmitter::GetNextByte(uint8_t& byte) {
    if (tx_buffer_.Pop(byte)) {
        stats_.bytes_transmitted++;
        return true;
    }
    return false;
}

} // namespace UART
} // namespace ReconRover
