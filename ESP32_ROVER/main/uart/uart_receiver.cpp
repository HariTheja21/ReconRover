#include "uart_receiver.h"

namespace ReconRover {
namespace UART {

UartReceiver::UartReceiver(UartStatistics& stats)
    : stats_(stats), state_(State::WAIT_HEADER_1), bytes_read_(0), packet_ready_(false) {}

void UartReceiver::ResetFramer() {
    state_ = State::WAIT_HEADER_1;
    bytes_read_ = 0;
}

uint8_t UartReceiver::CalculateCRC(const uint8_t* data, uint8_t length) {
    uint8_t crc = 0;
    for (uint8_t i = 0; i < length; ++i) {
        crc ^= data[i];
    }
    return crc;
}

void UartReceiver::ProcessByte(uint8_t byte) {
    stats_.bytes_received++;

    if (packet_ready_) {
        // Prevent overwriting if the engine hasn't pulled the last packet yet
        return; 
    }

    switch (state_) {
        case State::WAIT_HEADER_1:
            if (byte == 0xAA) {
                current_packet_[0] = byte;
                state_ = State::WAIT_HEADER_2;
            }
            break;

        case State::WAIT_HEADER_2:
            if (byte == 0x55) {
                current_packet_[1] = byte;
                bytes_read_ = 2;
                state_ = State::READ_PAYLOAD;
            } else {
                stats_.framing_errors++;
                ResetFramer();
            }
            break;

        case State::READ_PAYLOAD:
            current_packet_[bytes_read_++] = byte;
            
            // Assume strict 9-byte packets for Phase 4 architecture
            if (bytes_read_ == 9) {
                uint8_t crc = CalculateCRC(current_packet_, 8);
                if (crc == current_packet_[8]) {
                    packet_ready_ = true;
                    stats_.packets_received++;
                } else {
                    stats_.framing_errors++;
                }
                ResetFramer(); // Ready for next packet regardless of CRC pass/fail
            }
            break;
    }
}

bool UartReceiver::HasPacket() const {
    return packet_ready_;
}

bool UartReceiver::GetPacket(UartPacket& out_packet) {
    if (!packet_ready_) return false;
    
    out_packet.length = 9;
    for (int i=0; i<9; i++) {
        out_packet.buffer[i] = current_packet_[i];
    }
    packet_ready_ = false;
    return true;
}

} // namespace UART
} // namespace ReconRover
