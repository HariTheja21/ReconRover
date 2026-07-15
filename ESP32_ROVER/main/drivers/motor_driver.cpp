#include "motor_driver.h"

// Note: In real ESP-IDF, #include "driver/ledc.h" and "driver/gpio.h" would be here.

namespace ReconRover {
namespace Drivers {

MotorDriver::MotorDriver(DriverStatistics& stats) : stats_(stats) {}

void MotorDriver::Init() {
    // Configure LEDC timers and channels for ENA/ENB
    // Configure GPIOs for IN1, IN2, IN3, IN4 as outputs
}

int16_t MotorDriver::ScaleToPWM(int16_t velocity) {
    // Scale from [-32767, 32767] to 8-bit LEDC duty cycle [-255, 255]
    // Example: (velocity * 255) / 32767
    return static_cast<int16_t>((static_cast<int32_t>(velocity) * 255) / 32767);
}

void MotorDriver::SetLeftMotor(int16_t pwm) {
    // Hardware abstraction:
    // if pwm > 0: IN1 = HIGH, IN2 = LOW, ENA = pwm
    // if pwm < 0: IN1 = LOW, IN2 = HIGH, ENA = -pwm
    // if pwm == 0: IN1 = LOW, IN2 = LOW, ENA = 0
}

void MotorDriver::SetRightMotor(int16_t pwm) {
    // Hardware abstraction:
    // if pwm > 0: IN3 = HIGH, IN4 = LOW, ENB = pwm
    // if pwm < 0: IN3 = LOW, IN4 = HIGH, ENB = -pwm
    // if pwm == 0: IN3 = LOW, IN4 = LOW, ENB = 0
}

void MotorDriver::Drive(int16_t left_v, int16_t right_v) {
    int16_t l_pwm = ScaleToPWM(left_v);
    int16_t r_pwm = ScaleToPWM(right_v);

    SetLeftMotor(l_pwm);
    SetRightMotor(r_pwm);
    stats_.motor_commands_executed++;
}

void MotorDriver::EmergencyStop() {
    SetLeftMotor(0);
    SetRightMotor(0);
    stats_.estops_triggered++;
}

} // namespace Drivers
} // namespace ReconRover
