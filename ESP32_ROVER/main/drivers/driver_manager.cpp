#include "driver_manager.h"

namespace ReconRover {
namespace Drivers {

DriverManager::DriverManager()
    : motor_driver_(stats_),
      servo_driver_(stats_),
      oled_driver_(stats_),
      rgb_driver_(stats_),
      buzzer_driver_(stats_) {}

void DriverManager::InitAll() {
    motor_driver_.Init();
    servo_driver_.Init();
    oled_driver_.Init();
    rgb_driver_.Init();
    buzzer_driver_.Init();
}

void DriverManager::HandleMotorCommand(const Runtime::MotorCommandEvent& event) {
    motor_driver_.Drive(event.left_velocity, event.right_velocity);
}

void DriverManager::HandleServoCommand(const Runtime::ServoCommandEvent& event) {
    servo_driver_.SetAngle(event.servo_id, event.angle);
}

void DriverManager::HandleOLEDCommand(const Runtime::OLEDCommandEvent& event) {
    oled_driver_.SetDisplayMode(event.display_mode);
}

void DriverManager::HandleRGBCommand(const Runtime::RGBCommandEvent& event) {
    rgb_driver_.SetColor(event.r, event.g, event.b);
}

void DriverManager::HandleBuzzerCommand(const Runtime::BuzzerCommandEvent& event) {
    buzzer_driver_.PlayTone(event.frequency, event.duration_ms);
}

void DriverManager::HandleEmergencyStop(const Runtime::EmergencyStopEvent& event) {
    motor_driver_.EmergencyStop();
    rgb_driver_.SetColor(255, 0, 0); // Flash red
    buzzer_driver_.PlayTone(1000, 500); // Beep
}

} // namespace Drivers
} // namespace ReconRover
