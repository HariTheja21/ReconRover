#pragma once
#include <cstdint>
#include <cstddef>
#include "packet_receiver.h"
#include "packet_validator.h"
#include "command_router.h"
#include "command_dispatcher.h"
#include "runtime_statistics.h"

namespace ReconRover {
namespace Runtime {

class RuntimeEngine {
public:
    RuntimeEngine(CommandDispatcher& dispatcher);

    void ProcessIncomingBytes(const uint8_t* data, size_t length);
    
    RuntimeStatistics& GetStatistics() { return stats_; }

private:
    RuntimeStatistics stats_;
    PacketReceiver receiver_;
    PacketValidator validator_;
    CommandRouter router_;
    uint8_t packet_buffer_[PacketValidator::PACKET_LENGTH];
};

} // namespace Runtime
} // namespace ReconRover
