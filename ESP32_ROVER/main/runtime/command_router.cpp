#include "command_router.h"

namespace ReconRover {
namespace Runtime {

CommandRouter::CommandRouter(CommandDispatcher& dispatcher, RuntimeStatistics& stats)
    : dispatcher_(dispatcher), stats_(stats) {}

void CommandRouter::Route(const uint8_t* packet) {
    uint8_t cmd_type = packet[2];
    
    RuntimeEvent event;
    bool dispatch = false;

    if (cmd_type == CMD_WHEEL_VELOCITY) {
        // Parse left and right velocities (Big-Endian)
        int16_t left_v = (packet[4] << 8) | packet[5];
        int16_t right_v = (packet[6] << 8) | packet[7];

        if (left_v == 0 && right_v == 0 && packet[3] == 99) { 
            // Optional: Treat specific sequence/target as E-Stop if defined as such,
            // Or just a standard velocity. The Python side uses seq 99 and 0,0 for E-Stop.
            // We can emit both or just MOTOR_COMMAND. We'll emit MOTOR_COMMAND for now,
            // and the motor controller will naturally stop.
            // If explicit E-Stop command type existed, we'd route to EMERGENCY_STOP.
        }

        event.type = EventType::MOTOR_COMMAND;
        event.payload.motor.left_velocity = left_v;
        event.payload.motor.right_velocity = right_v;
        dispatch = true;
    }
    // else if (cmd_type == ...) { }

    if (dispatch) {
        dispatcher_.Dispatch(event);
        stats_.events_dispatched++;
    }
}

} // namespace Runtime
} // namespace ReconRover
