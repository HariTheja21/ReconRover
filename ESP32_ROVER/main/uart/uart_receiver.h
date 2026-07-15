#pragma once
#include "uart_events.h"
#include "uart_buffer.h"
#include "uart_statistics.h"

namespace ReconRover {
namespace UART {

class UartReceiver {
public:
    UartReceiver(UartStatistics& stats);

    // Feeds bytes from the hardware UART into the framing state machine
    void ProcessByte(uint8_t byte);

    // Checks if a full valid packet has been framed
    bool HasPacket() const;

    // Retrieves the framed packet
    bool GetPacket(UartPacket& out_packet);

private:
    UartStatistics& stats_;
    UartBuffer<256> rx_buffer_;
    
    enum class State { WAIT_HEADER_1, WAIT_HEADER_2, READ_PAYLOAD };
    State state_;
    uint8_t current_packet_[UartPacket::MAX_LENGTH];
    uint8_t bytes_read_;
    bool packet_ready_;

    void ResetFramer();
    uint8_t CalculateCRC(const uint8_t* data, uint8_t length);
};

} // namespace UART
} // namespace ReconRover
