#pragma once
#include "uart_events.h"
#include "uart_buffer.h"
#include "uart_statistics.h"

namespace ReconRover {
namespace UART {

class UartTransmitter {
public:
    UartTransmitter(UartStatistics& stats);

    // Queues a packet for transmission
    bool QueuePacket(const UartPacket& packet);

    // Extracts bytes to push to the physical UART hardware driver
    bool GetNextByte(uint8_t& byte);

private:
    UartStatistics& stats_;
    UartBuffer<256> tx_buffer_;
};

} // namespace UART
} // namespace ReconRover
