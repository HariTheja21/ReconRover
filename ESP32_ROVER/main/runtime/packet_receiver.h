#pragma once
#include <cstdint>
#include <cstddef>
#include "packet_validator.h"

namespace ReconRover {
namespace Runtime {

class PacketReceiver {
public:
    static constexpr size_t BUFFER_SIZE = 256;
    
    PacketReceiver();

    // Ingests incoming bytes from UART. Returns true if a full packet was extracted.
    bool ProcessBytes(const uint8_t* data, size_t length, uint8_t* out_packet);

private:
    uint8_t buffer_[BUFFER_SIZE];
    size_t head_;
    size_t tail_;
    size_t count_;

    void Push(uint8_t b);
    uint8_t Peek(size_t offset) const;
    void Consume(size_t amount);
};

} // namespace Runtime
} // namespace ReconRover
