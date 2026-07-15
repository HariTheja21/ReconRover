#pragma once
#include <cstdint>
#include "driver_statistics.h"

namespace ReconRover {
namespace Drivers {

class RGBDriver {
public:
    RGBDriver(DriverStatistics& stats);
    void Init();
    
    void SetColor(uint8_t r, uint8_t g, uint8_t b);

private:
    DriverStatistics& stats_;
};

} // namespace Drivers
} // namespace ReconRover
