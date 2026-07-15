#pragma once
#include <cstdint>

namespace ReconRover {
namespace Drivers {

struct MotorStatusEvent {
    bool is_driving;
    int16_t current_left_pwm;
    int16_t current_right_pwm;
};

struct ServoStatusEvent {
    uint8_t servo_id;
    int16_t current_angle;
};

struct DriverHealthEvent {
    bool all_healthy;
    bool motor_fault;
    bool i2c_bus_fault; // OLED
};

} // namespace Drivers
} // namespace ReconRover
