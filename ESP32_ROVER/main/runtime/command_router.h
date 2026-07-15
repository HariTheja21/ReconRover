#pragma once
#include <cstdint>
#include "command_dispatcher.h"
#include "runtime_statistics.h"

namespace ReconRover {
namespace Runtime {

class CommandRouter {
public:
    static constexpr uint8_t CMD_WHEEL_VELOCITY = 0x01;
    // Add other command IDs as needed (0x02 for servos, etc.)

    CommandRouter(CommandDispatcher& dispatcher, RuntimeStatistics& stats);

    void Route(const uint8_t* packet);

private:
    CommandDispatcher& dispatcher_;
    RuntimeStatistics& stats_;
};

} // namespace Runtime
} // namespace ReconRover
