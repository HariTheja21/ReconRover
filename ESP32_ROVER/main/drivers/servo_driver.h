#pragma once
#include <cstdint>
#include "driver_statistics.h"

namespace ReconRover {
namespace Drivers {

class ServoDriver {
public:
    ServoDriver(DriverStatistics& stats);
    void Init();
    
    // Angle bounded to physical limits (e.g., 0 to 180 degrees)
    void SetAngle(uint8_t servo_id, int16_t angle);

private:
    DriverStatistics& stats_;
    int16_t ClampAngle(int16_t angle);
};

} // namespace Drivers
} // namespace ReconRover
