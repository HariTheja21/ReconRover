#include "servo_driver.h"

namespace ReconRover {
namespace Drivers {

ServoDriver::ServoDriver(DriverStatistics& stats) : stats_(stats) {}

void ServoDriver::Init() {
    // Configure LEDC for 50Hz PWM signal (20ms period) suitable for SG90 servos
}

int16_t ServoDriver::ClampAngle(int16_t angle) {
    if (angle < 0) return 0;
    if (angle > 180) return 180;
    return angle;
}

void ServoDriver::SetAngle(uint8_t servo_id, int16_t angle) {
    int16_t safe_angle = ClampAngle(angle);
    
    // Hardware abstraction:
    // Convert angle [0, 180] to duty cycle [min_duty, max_duty]
    // ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty);
    // ledc_update_duty(LEDC_MODE, LEDC_CHANNEL);

    stats_.servo_commands_executed++;
}

} // namespace Drivers
} // namespace ReconRover
