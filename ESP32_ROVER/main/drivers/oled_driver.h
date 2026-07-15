#pragma once
#include <cstdint>
#include "driver_statistics.h"

namespace ReconRover {
namespace Drivers {

class OLEDDriver {
public:
    OLEDDriver(DriverStatistics& stats);
    void Init();
    
    // Updates display based on abstract mode
    void SetDisplayMode(uint8_t mode);

private:
    DriverStatistics& stats_;
};

} // namespace Drivers
} // namespace ReconRover
