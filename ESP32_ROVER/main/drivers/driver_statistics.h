#pragma once
#include <cstdint>

namespace ReconRover {
namespace Drivers {

struct DriverStatistics {
    uint32_t motor_commands_executed = 0;
    uint32_t servo_commands_executed = 0;
    uint32_t oled_updates = 0;
    uint32_t rgb_updates = 0;
    uint32_t buzzer_tones = 0;
    uint32_t estops_triggered = 0;
};

} // namespace Drivers
} // namespace ReconRover
