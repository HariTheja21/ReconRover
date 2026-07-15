#pragma once
#include <cstdint>

namespace ReconRover {
namespace UART {

// A static ring buffer to prevent dynamic allocation
template <uint16_t SIZE>
class UartBuffer {
public:
    UartBuffer() : head_(0), tail_(0), count_(0) {}

    bool Push(uint8_t byte) {
        if (count_ >= SIZE) {
            return false;
        }
        buffer_[head_] = byte;
        head_ = (head_ + 1) % SIZE;
        count_++;
        return true;
    }

    bool Pop(uint8_t& byte) {
        if (count_ == 0) {
            return false;
        }
        byte = buffer_[tail_];
        tail_ = (tail_ + 1) % SIZE;
        count_--;
        return true;
    }

    bool IsEmpty() const { return count_ == 0; }
    bool IsFull() const { return count_ >= SIZE; }
    uint16_t Count() const { return count_; }

private:
    uint8_t buffer_[SIZE];
    uint16_t head_;
    uint16_t tail_;
    uint16_t count_;
};

} // namespace UART
} // namespace ReconRover
