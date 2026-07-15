#pragma once
#include <cstdint>
#include "driver_statistics.h"

namespace ReconRover {
namespace Drivers {

class MotorDriver {
public:
    // Physical pin mappings would go here (e.g., IN1, IN2, ENA, IN3, IN4, ENB)
    
    MotorDriver(DriverStatistics& stats);
    void Init();
    
    // Accepts velocities bounded between -32767 and +32767
    void Drive(int16_t left_v, int16_t right_v);
    
    void EmergencyStop();

private:
    DriverStatistics& stats_;
    int16_t ScaleToPWM(int16_t velocity);
    void SetLeftMotor(int16_t pwm);
    void SetRightMotor(int16_t pwm);
};

} // namespace Drivers
} // namespace ReconRover
