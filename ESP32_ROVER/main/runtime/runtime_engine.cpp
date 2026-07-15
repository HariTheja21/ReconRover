#include "runtime_engine.h"

namespace ReconRover {
namespace Runtime {

RuntimeEngine::RuntimeEngine(CommandDispatcher& dispatcher)
    : receiver_(),
      validator_(stats_),
      router_(dispatcher, stats_) {}

void RuntimeEngine::ProcessIncomingBytes(const uint8_t* data, size_t length) {
    stats_.bytes_processed += length;

    // The receiver will pull full 9-byte packets out of the stream.
    // There could be multiple packets in one chunk of bytes, so we loop.
    while (receiver_.ProcessBytes(data, length, packet_buffer_)) {
        // Only pass data once per call to ProcessBytes, subsequent loop iterations 
        // will just process whatever is left in the receiver's internal buffer.
        data = nullptr; 
        length = 0;
        
        stats_.packets_received++;

        if (validator_.Validate(packet_buffer_, PacketValidator::PACKET_LENGTH)) {
            router_.Route(packet_buffer_);
        }
    }
}

} // namespace Runtime
} // namespace ReconRover
