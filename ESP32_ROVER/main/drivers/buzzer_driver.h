#pragma once
#include <cstdint>
#include "driver_statistics.h"

namespace ReconRover {
namespace Drivers {

class BuzzerDriver {
public:
    BuzzerDriver(DriverStatistics& stats);
    void Init();
    
    void PlayTone(uint16_t frequency, uint16_t duration_ms);

private:
    DriverStatistics& stats_;
};

} // namespace Drivers
} // namespace ReconRover
