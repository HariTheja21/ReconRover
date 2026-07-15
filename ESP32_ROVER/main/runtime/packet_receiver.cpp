#include "packet_receiver.h"

namespace ReconRover {
namespace Runtime {

PacketReceiver::PacketReceiver() : head_(0), tail_(0), count_(0) {}

void PacketReceiver::Push(uint8_t b) {
    if (count_ < BUFFER_SIZE) {
        buffer_[tail_] = b;
        tail_ = (tail_ + 1) % BUFFER_SIZE;
        count_++;
    }
}

uint8_t PacketReceiver::Peek(size_t offset) const {
    if (offset >= count_) return 0;
    return buffer_[(head_ + offset) % BUFFER_SIZE];
}

void PacketReceiver::Consume(size_t amount) {
    if (amount > count_) amount = count_;
    head_ = (head_ + amount) % BUFFER_SIZE;
    count_ -= amount;
}

bool PacketReceiver::ProcessBytes(const uint8_t* data, size_t length, uint8_t* out_packet) {
    for (size_t i = 0; i < length; ++i) {
        Push(data[i]);
    }

    // Try to frame a packet
    while (count_ >= PacketValidator::PACKET_LENGTH) {
        if (Peek(0) == PacketValidator::HEADER_1 && Peek(1) == PacketValidator::HEADER_2) {
            // Found a header, copy packet
            for (size_t i = 0; i < PacketValidator::PACKET_LENGTH; ++i) {
                out_packet[i] = Peek(i);
            }
            Consume(PacketValidator::PACKET_LENGTH);
            return true;
        } else {
            // Not a header, drop 1 byte and search again
            Consume(1);
        }
    }
    
    // Check if we need to drop junk bytes when buffer gets full without a header
    if (count_ > 0 && Peek(0) != PacketValidator::HEADER_1) {
        Consume(1);
    }

    return false;
}

} // namespace Runtime
} // namespace ReconRover
